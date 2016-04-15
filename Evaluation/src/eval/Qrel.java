package eval;

public class Qrel {
	String document_id ;
	int topic_no ;
	int subtopic_no ;
	public int judgment ;
	
	/*
	 * Initialize the Qrel object with query, document and 
	 * its relevance grade.
	 */
	public Qrel(String topic, String doc_id, String rel) {
        topic_no=Integer.parseInt(topic);
        document_id=doc_id;
        judgment=Integer.parseInt(rel);
		
	}

	/*
	 * Initialize the Qrel object with query, subtopic, document and 
	 * its relevance grade with respect to query subtopic.
	 */
	public Qrel(String topic, String subtopic,  String doc_id, String rel) {
        this(topic,doc_id,rel);
        subtopic_no=Integer.parseInt(subtopic);
	}
	
	public String getDocumentId()
	{
		return document_id;
	}
    
    public int getJudgement()
    {
        return judgment;
    }
	
	public int getTopicNo()
	{
		return topic_no;
	}

	public int getSubtopicNo()
	{
		return subtopic_no;
	}
}
