
public class Main {

    static void main(String[] args){
    
        NewsAgency observable = new NewsAgency();
        NewsChannel observer = new NewsChannel();

        observable.addObserver(observer);   
        observable.setNews("news");
        assertEquals(observer.getNews(), "news");
        
    }
}
    