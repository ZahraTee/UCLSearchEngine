package eval;

public class Result {
	  String document_id;
	  int document_rank;
	  double score;
	  
    public Result(String document_id,int document_rank,double score)
    {
        this.document_id=document_id;
        this.document_rank=document_rank;
        this.score=score;
    }
    
    public void setDocumentId(String document_id)
    {
        this.document_id=document_id;
    }
    public String getDocumentId()
    {
        return document_id;
    }
    public void setDocumentRank(int document_rank)
    {
        this.document_rank=document_rank;
    }
    public int getDocumentRank()
    {
        return document_rank;
    }
    public void setDocumentScore(double score)
    {
        this.score=score;
    }
    public double getDocumentScore()
    {
        return score;
    }
    
	}
