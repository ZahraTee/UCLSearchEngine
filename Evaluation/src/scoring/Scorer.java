package scoring;

import java.io.File;
import java.io.FileNotFoundException;
import java.io.FileReader;
import java.io.IOException;
import java.io.PrintWriter;
import java.util.ArrayList;
import java.util.Collections;
import java.util.Comparator;
import java.util.HashMap;
import java.util.HashSet;
import java.util.Map.Entry;
import java.util.Scanner;

import org.terrier.applications.batchquerying.TRECQuery;
import org.terrier.matching.ResultSet;
import org.terrier.querying.Manager;
import org.terrier.querying.SearchRequest;
import org.terrier.structures.DocumentIndex;
import org.terrier.structures.Index;
import org.terrier.structures.Lexicon;
import org.terrier.utility.ApplicationSetup;

import eval.NDCG;
import eval.Qrel;
import eval.Result;
import utils.Utils;

public class Scorer {
	/* Terrier Index */
	Index index;
	
	/* Index structures*/
	/* list of terms in the index */
	Lexicon<String> term_lexicon = null;
	/* list of documents in the index */
	DocumentIndex doi = null;
	
	/* Collection statistics */
	long total_tokens;
	long total_documents;
	
	final double POWER = 0.102;
	
	String[] URLs;
	HashMap<String,Integer> URLIndexMap;
	double[] PageRank;
	
	/* Initialize Simple model with index. Use 
	 * @param index_path : initialize index 
	 * @param prefix : language prefix for index 
	 * with location of index created using bash script.
	 */
	public Scorer(String index_path, String prefix,String urls_path,String page_rank_path) {
		
		// Load the index and collection stats
		try {
			loadURLsAndPageRanks(urls_path,page_rank_path);
			index = Index.createIndex(index_path, prefix);
			
			System.out.println("Loaded index from path "+index_path+" "+index.toString());
			total_tokens = index.getCollectionStatistics().getNumberOfTokens();
			total_documents = index.getCollectionStatistics().getNumberOfDocuments();
			System.out.println("Number of terms and documents in index "+total_tokens+" "+total_documents);
			
	
		}
		catch(Exception ex)
		{
			ex.printStackTrace();
		}
	}
	
	private void loadURLsAndPageRanks(String urls_path,String page_rank_path) throws FileNotFoundException
	{
		//Stores the URL of document with id x in URLs[x]
		URLs = new String[200891];
		//Map from URL to index
		URLIndexMap = new HashMap<String,Integer>();
		PageRank = new double[200891];
		Scanner url = new Scanner(new FileReader(urls_path));
		Scanner pr = new Scanner(new FileReader(page_rank_path));
		for(int n=0;n<URLs.length;n++)
		{
			URLs[n]=url.nextLine();
			URLIndexMap.put(URLs[n],n);
			PageRank[n]=pr.nextDouble();
		}
		url.close();
		pr.close();
	}
	
	public HashMap <String, Double> buildResultSet(String id, String query){
		// Just find documents and their posting list for the query. 
		
		
		// Create a search request object.
		Manager manager = new Manager(this.index);
		SearchRequest srq = manager.newSearchRequest(id, query);
		
		// Get the results using bm25
		srq.addMatchingModel("Matching", "BM25");
		manager.runPreProcessing(srq);
		manager.runMatching(srq);
		manager.runPostProcessing(srq);
		manager.runPostFilters(srq);
		
		ResultSet set = srq.getResultSet();
		double doc_scores [] = set.getScores();
		
		final String metaIndexDocumentKey = ApplicationSetup.getProperty(
				"trec.querying.outputformat.docno.meta.key", "filename");
		String doc_names [] = Utils.getDocnos(metaIndexDocumentKey, set, index);
		
		
		HashMap <String, Double> scores = new HashMap<String, Double>();
		for (int i = 0 ; i < doc_scores.length;i++){
			int n = Integer.parseInt(doc_names[i].substring(12, doc_names[i].length()-4));
			scores.put(URLs[n], doc_scores[i]*Math.pow(PageRank[n],POWER));
		}
			
		
		return scores;
		
	}
	public void closeIndex() {
		try {
			index.close();
		} catch (IOException e) {
			// TODO Auto-generated catch block
			e.printStackTrace();
		}
	}

	static ArrayList<ArrayList<Qrel>> loadQrels(String[] judgment_file_name,String relevance_judgments_path) throws IOException
	{
		ArrayList<ArrayList<Qrel>> qrels = new ArrayList<ArrayList<Qrel>>();
		qrels.add(null);
		for(int i=1;i<=50;i++)
		{
			ArrayList<Qrel> tt = new ArrayList<Qrel>();

				Scanner qrel = new Scanner(new FileReader(relevance_judgments_path+judgment_file_name[i]));
				while(qrel.hasNext())
				{
					qrel.nextInt();
					String u = qrel.next();
					int j =qrel.nextInt();
		
					Qrel q = new Qrel(""+1,u,""+j);
					tt.add(q);
				}
				qrel.close();
			
			qrels.add(tt);
		}
		return qrels;
	}
	public static void main(String [] args) throws IOException {
		
		
		String path = System.getProperty("user.dir");
		path = path.substring(0, path.length()-10);
		System.setProperty("terrier.home", path+"terrier-core-4.1");
		
		// Topic file path
		String topic_file_path = path+"tagged_queries.txt";
		
		// Index path
		String index_path = path+"terrier-core-4.1/var/index/";
		
		// URLs path
		String url_path = path+"search-api/URLs.txt";
		
		//Page Rank path
		String page_rank_path = path+"PageRank.txt";
		
		//Relevance Judgments path
		String relevance_judgments_path = path+"search-api/judgement_results/";
		
		//Google results path
		String google_results_path=path+"search-api/ordered_links_google/";
		
		//UCL results path
		String ucl_results_path=path+"search-api/ordered_links_ucl/";
		
		//Loads UCL & Google results
		ArrayList<ArrayList<Result>> ucl_results = new ArrayList<ArrayList<Result>>();
		ArrayList<ArrayList<Result>> google_results = new ArrayList<ArrayList<Result>>();
		ucl_results.add(null);
		google_results.add(null);
		for(int i=1;i<=50;i++)
			for(int j=0;j<2;j++)
			{			
				ArrayList<Result> list= new ArrayList<Result>();
				HashSet<String> links = new HashSet<String>();
				Scanner in = new Scanner(new FileReader((j==0?ucl_results_path:google_results_path)+"query_"+i+".txt"));
				int n =1;
				while(in.hasNext())
				{
					String link = in.nextLine();
					if(!links.contains(link))
						list.add(new Result(link,n++,n));
				}
				in.close();
				if(j==0)
					ucl_results.add(list);
				else
					google_results.add(list);
				
			}
			
		
		
		//Names of the files containing relevance judgments
		String judgment_file_name[] = new String[51];
		File dir = new File(relevance_judgments_path);
		for (File child : dir.listFiles()) 
		{
			String name = child.getName();
			if (name.length()>16 &&"judgement.query_".equals(name.substring(0, 16))) 
			{
				String str = name.substring(16, 18);
				if(str.charAt(1)=='.')
					str=str.substring(0,1);
				int n = Integer.parseInt(str);
				judgment_file_name[n]=name;
			}
		}
		
		
				
		//Load Qrels
		ArrayList<ArrayList<Qrel>> qrels =loadQrels(judgment_file_name,relevance_judgments_path);
		
		// Load the topics
		TRECQuery trec_topics = new TRECQuery(topic_file_path);
						
		// Initialize the scorer
		Scorer scorer = new Scorer(index_path, "ucl_search_engine",url_path,page_rank_path);
		
		int nextId=0;
		
		int K[] = new int[]{1,2,5,10,20};
		double ndcg[][][] = new double[3][K.length][51];
		double average_ndcg[][] = new double[3][K.length];

		for(int q=1;q<=50;q++)
		{
			String query = trec_topics.next();
				
			HashMap<String, Double> scores = scorer.buildResultSet(nextId+++"", query);
						
			ArrayList<Entry<String,Double>> ent = new ArrayList<Entry<String,Double>>(scores.entrySet());
				
			
			Collections.sort(ent,new Comparator<Entry<String,Double>>(){
		
					@Override
					public int compare(Entry<String, Double> o1,
							Entry<String, Double> o2) {
						
						return o2.getValue().compareTo(o1.getValue());
					}});
			ArrayList<Result> our_results = new ArrayList<Result>();
			for(int i=0;i<20&&i<ent.size();i++)
				our_results.add(new Result(ent.get(i).getKey(),i+1,ent.get(i).getValue()));
			
			for(int k=0;k<K.length;k++)
			{
				ndcg[0][k][q]=NDCG.compute(google_results.get(q), qrels.get(q), K[k]);
				ndcg[1][k][q]=NDCG.compute(ucl_results.get(q), qrels.get(q), K[k]);
				ndcg[2][k][q]=NDCG.compute(our_results, qrels.get(q), K[k]);
				for(int i=0;i<3;i++)
					average_ndcg[i][k]+=0.02*ndcg[i][k][q];
			}
		}
		PrintWriter writer = new PrintWriter(path+"ndcg_results.txt", "UTF-8");
		writer.println("Average NDCGs:");
		writer.println("Engine  \tNDCG@1\tNDCG@2\tNDCG@5\tNDCG@10\tNDCG@20\n");
		for(int i=0;i<3;i++)
			writer.printf("%s\t%5.3f\t%5.3f\t%5.3f\t%5.3f\t%5.3f\n",i==0?"Google's":i==1?"UCL's   ":"Ours    "
				,average_ndcg[i][0],average_ndcg[i][1],average_ndcg[i][2],average_ndcg[i][3],average_ndcg[i][4]);
		for(int q=1;q<=50;q++)
		{
			writer.println("\nQuery "+q+":");
			writer.println("Engine  \tNDCG@1\tNDCG@2\tNDCG@5\tNDCG@10\tNDCG@20\n");
			for(int i=0;i<3;i++)
				writer.printf("%s\t%5.3f\t%5.3f\t%5.3f\t%5.3f\t%5.3f\n",i==0?"Google's":i==1?"UCL's   ":"Ours    "
					,ndcg[i][0][q],ndcg[i][1][q],ndcg[i][2][q],ndcg[i][3][q],ndcg[i][4][q]);
		}
		writer.close();
	}


}
