package eval;

import java.util.ArrayList;
import java.util.Collections;
import java.util.Comparator;
import java.util.HashMap;


public class NDCG {

	private NDCG () {}
	
	
	/* *
	@param retrieved_list : list of documents, 
	the highest - ranking document first .
	@param qrel_list : a collection of labelled 
	document ids from qrel .
	@param k : cut - off for calculation of NDCG@k
	@return the NDCG for given data
	*/
	
	public static double compute (ArrayList <Result> retrieved_list ,ArrayList <Qrel> qrel_list , int k ) {
		// A map for each document id -> relevance judgment
		HashMap<String,Integer> map = new HashMap<String,Integer>();
		for(Qrel q:qrel_list)
			map.put(q.getDocumentId(), q.getJudgement());
		// Relevance judgment for the top k retrieved documents
		double rel[] = new double[k];
		for(int i=0;i<k && i<retrieved_list.size();i++)
		{
			String key = retrieved_list.get(i).getDocumentId();
			if(map.containsKey(key))
				rel[i]=map.get(key);
			else
				rel[i]=0;
			
		}
		double tmp1 = DCG(rel);
		double tmp2 = computeIDCG(qrel_list,k);
		if(tmp2==0)
			return 0;
		return tmp1/tmp2;
		
	}
	
	//Computes the DCG for given relavance order
	private static double DCG(double[] rel)
	{
		double rst = rel[0];
		for(int i=1;i<rel.length;i++)
			rst+=rel[i]/(Math.log(i+1)/Math.log(2));
		return rst;
	}
	
	static double computeIDCG ( ArrayList <Qrel> qrel_list ,int k) {
		//Order Qrels from highest relavent to least relavent
		class CMP implements Comparator<Qrel>
		{

			@Override
			public int compare(Qrel o1, Qrel o2) {
				return o2.judgment-o1.judgment;
			}
			
		}
		Collections.sort(qrel_list,new CMP());
		//Computed DCG on this relavance order
		double[] rel = new double[k];
		for(int i=0;i<k && i<qrel_list.size();i++)
			rel[i]=qrel_list.get(i).getJudgement();
		return DCG(rel);
	}
}
