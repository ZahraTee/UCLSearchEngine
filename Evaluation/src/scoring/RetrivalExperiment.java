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

public class RetrivalExperiment {
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
	
	
	static String[] URLs;
	static HashMap<String,Integer> URLIndexMap;
	static double[] PageRank;
	final String originalModel;
	
	/* Initialize Simple model with index. Use 
	 * @param index_path : initialize index 
	 * @param prefix : language prefix for index 
	 * with location of index created using bash script.
	 */
	public RetrivalExperiment(String index_path, String prefix,String originalModel) {
		
		// Load the index and collection stats
		this.originalModel=originalModel;
		try {
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
	
	static void loadURLsAndPageRanks(String urls_path,String page_rank_path) throws FileNotFoundException
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
	
	public static double newScore(double oldScore,double pageRank,double[] params)
	{
		return oldScore*pageRank*params[0]+oldScore*params[1]+pageRank*params[2];
	}
	
	public HashMap <String, Double> buildResultSet(String id, String query){
		// Just find documents and their posting list for the query. 
		
		
		// Create a search request object.
		Manager manager = new Manager(this.index);
		SearchRequest srq = manager.newSearchRequest(id, query);
		
		// Get the results using bm25
		srq.addMatchingModel("Matching", originalModel);
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
			scores.put(URLs[n], doc_scores[i]);
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
	
	static boolean incr(double[] mine,double maxLimit[],double minLimit[],double step[])
	{
		int n = mine.length;
		do
		{
			n--;
			mine[n]+=step[n];
			if(mine[n]<=maxLimit[n])
				break;
			mine[n]=minLimit[n];
		}while(n>0);
		return !(n==0 && mine[0]==minLimit[0]);
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
		loadURLsAndPageRanks(url_path,page_rank_path);
		
				
		//Load Qrels
		ArrayList<ArrayList<Qrel>> qrels =loadQrels(judgment_file_name,relevance_judgments_path);
		
		// Load the topics
		TRECQuery trec_topics = new TRECQuery(topic_file_path);
						
		// Configure These
		String originalModel = "BM25";
		double minLimit[] = new double[]{0.0,0.0,0.0};
		double maxLimit[] = new double[]{1.0,1.0,10000.0};
		double step[] = new double[]{0.1,0.1,1000.0};
		
		RetrivalExperiment scorer = new RetrivalExperiment(index_path, "ucl_search_engine",originalModel);
		int nextId=0;
		ArrayList<HashMap<String,Double>> allScores = new ArrayList<HashMap<String,Double>>();
		allScores.add(null);
		for(int q=1;q<=50;q++)
		{
			String query = trec_topics.next();
			allScores.add(scorer.buildResultSet(nextId+++"", query));
		}
		
		int n=0;
		
		double maxNDCG=-1;
		double best[] = new double[step.length];
		
		double cur[] = new double[step.length];
		for(int i=0;i<cur.length;i++)
			cur[i]=minLimit[i];
		
		
		do
		{
			n++;
			double ndcg=0;
			for(int q=1;q<=50;q++)
			{	
					
				HashMap<String, Double> scores = new HashMap<String,Double>();
				for(Entry<String,Double> e:allScores.get(q).entrySet())
					scores.put(e.getKey(), newScore(e.getValue(),PageRank[URLIndexMap.get(e.getKey())],cur));
							
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
				
				ndcg+=NDCG.compute(our_results, qrels.get(q), 20);
			}
			ndcg*=0.02;
			if(ndcg>maxNDCG)
			{
				maxNDCG=ndcg;
				for(int i=0;i<cur.length;i++)
					best[i]=cur[i];
			}
		}while(incr(cur,maxLimit,minLimit,step));
		System.out.println("Explored "+n+" Combinations");
		System.out.println("Best Average NDCG = "+maxNDCG);
		System.out.println("By parameters:");
		for(int i=0;i<best.length;i++)
			System.out.print(best[i]+(i==best.length-1?"\n":" "));
	}


}
