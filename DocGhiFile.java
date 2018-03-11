import java.io.BufferedReader;
import java.io.File;
import java.io.FileReader;
import java.io.FileWriter;
import java.io.IOException;
import java.util.ArrayList;

import org.omg.CosNaming.NamingContextExtPackage.StringNameHelper;

public class DocGhiFile {

	public void write(String url, String data){
		try {
			//Bước 1: Tạo đối tượng luồng và liên kết nguồn dữ liệu
			File f = new File(url);
			FileWriter fw = new FileWriter(f,true);

			//Bước 2: Ghi dữ liệu
			fw.write(data + "\r\n");

			//Bước 3: Đóng luồng
			fw.close(); 
		} catch (IOException ex) {
			System.out.println("Loi ghi file: " + ex);
		}
	}
	public ArrayList<String> readLinkNews(String url){

		ArrayList<String> listLinksNews = new ArrayList<>();
		try {
			//Bước 1: Tạo đối tượng luồng và liên kết nguồn dữ liệu
			File f = new File(url);
			FileReader fr = new FileReader(f);

			//Bước 2: Đọc dữ liệu
			BufferedReader br = new BufferedReader(fr);
			String line;
			while ((line = br.readLine()) != null){
				//System.out.println(line);
				//getNews.getLinksNews(line);
				listLinksNews.add(line);
			}

			//Bước 3: Đóng luồng
			fr.close();
			br.close(); 

		} catch (Exception ex) {
			System.out.println("Loi doc file: "+ex);
		}
		return listLinksNews;
	}
	
	public StringBuffer readFileToGetNoun(String url){

		StringBuffer str = new StringBuffer("");
		try {
			//Bước 1: Tạo đối tượng luồng và liên kết nguồn dữ liệu
			File f = new File(url);
			FileReader fr = new FileReader(f);

			//Bước 2: Đọc dữ liệu
			BufferedReader br = new BufferedReader(fr);
			String line;
			while ((line = br.readLine()) != null){
				String[] a ;
				//System.out.println(s.indexOf("hello"));
				if(line.indexOf("pos=\"N\"")>=0){
					a = line.split(">");
					str.append((a[1].split("<"))[0]+"\r\n");
				}
				
			}

			//Bước 3: Đóng luồng
			fr.close();
			br.close(); 

		} catch (Exception ex) {
			System.out.println("Loi doc file: "+ex);
		}
		return str;
	}
	public static void main(String[] args) {
		DocGhiFile obj = new DocGhiFile();
		ArrayList<String> arr = obj.readLinkNews("E:/Data_crawl/linkNews.txt");
		GetDocumentFromURL getNews = new GetDocumentFromURL();
		for(String url : arr){
			getNews.getMainHTML(url);
		}
	}
}






