import java.io.IOException;
import java.sql.Connection;

import org.jsoup.Jsoup;
import org.jsoup.nodes.Document;
import org.jsoup.nodes.Element;
import org.jsoup.select.Elements;

public class GetDocumentFromURL {

	static int nameNum = 0;
	//lấy nội dung bài viết
	public void getMainHTML(String url ){

		try {
			Document doc =  Jsoup.connect(url).get();
			DocGhiFile writer = new DocGhiFile();
			String name = "E:/Data_crawl/news/"+ nameNum + ".txt";
			//String title = doc.title();
			//System.out.println("Title : " + title);
			Element ele = doc.getElementsByClass("title_news").first();
			String title= ele.select("> h1").first().text();
			writer.write(name,title+"\r\n");
			Elements elements = doc.getElementsByClass("Normal");
			for( Element e : elements){
				
				//System.out.println(e.text()+"\n");
				writer.write(name,e.text()+"\r\n");
			}
			nameNum++;
		} catch (Exception e) {
			System.out.println("Connection error");
		}
	}

	//lấy link các bài viêt trong trang
	public void getLinksNews(String url){
		String fileName = "E:/Data_crawl/linkNews.txt";
		try {			
			DocGhiFile writer = new DocGhiFile();
			Document doc = Jsoup.connect(url).get();
			Elements h3Elements = doc.getElementsByClass("title_news");
			for (Element h3Element : h3Elements) {
				Element aElement = h3Element.select("> a").first();
				String href = aElement.attr("href");
				writer.write(fileName,href +"\r\n");
			}
		} catch (Exception e) {
			System.out.println("Connection error");
		}
	}
	//lấy link các thể loại tin tức
	public void getLinksCategory(){
		try {
			//http://vnexpress.net/tin-tuc/giao-duc/page/3.html
			String fileName = "E:/Data_crawl/linkMenu.txt";
			DocGhiFile writer = new DocGhiFile();
			Document doc = Jsoup.connect("http://vnexpress.net/").get();
			Element menuElement = doc.getElementById("menu_web");
			Elements aElements = menuElement.select("a");
			Elements aEclipses = aElements.select("[class^=mnu_]");
			for (Element aEclipse : aEclipses) {
				String href = aEclipse.attr("href");
				if(href.startsWith("http://")){
					//System.out.println("\n" + href);
					if(href.endsWith("/")){
						for(int i=1;i<=5;i++){
							writer.write(fileName,href + "page/"+i+".html\r\n");
						}
					}else{
						for(int i=1;i<=5;i++){
							writer.write(fileName,href + "/page/"+i+".html\r\n");
						}
					}

				}
				else{
					//System.out.println("\nhttp://vnexpress.net" + href);
					for(int i=1;i<=5;i++){
						writer.write(fileName,"http://vnexpress.net" + href +"/page/"+i+".html\r\n");
					}
				}
			}
		} catch (Exception e) {
			System.out.println("Connection error");
		}
	}
	public static void main(String[] args) throws IOException {
		GetDocumentFromURL obj = new GetDocumentFromURL();
		//String url = "http://vnexpress.net/tin-tuc/phap-luat/"
		//+ "ngay-mai-cuu-chu-tich-oceanbank-cung-47-bi-cao-hau-toa-3546720.html";
		//obj.getMainHTML(url);
		//obj.getLinksCategory();
		Document doc =  Jsoup.connect("http://kinhdoanh.vnexpress.net/tin-tuc/doanh-nghiep/thu-tuong-yeu-cau-dung-du-an-thep-ca-na-3570948.html").get();
		//String title = doc.title();
		Element e = doc.getElementsByClass("title_news").first();
		String title= e.select("> h1").first().text();
		System.out.println(title);
		obj.getMainHTML("http://kinhdoanh.vnexpress.net/tin-tuc/doanh-nghiep/thu-tuong-yeu-cau-dung-du-an-thep-ca-na-3570948.html");
	}

}