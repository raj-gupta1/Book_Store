package selenium_site;

import org.openqa.selenium.By;
import org.openqa.selenium.JavascriptExecutor;
import org.openqa.selenium.WebDriver;
import org.openqa.selenium.chrome.ChromeDriver;

public class sel_testing{

	public static void main(String[] args) throws InterruptedException{
		System.setProperty("webdriver.chrome.driver", "C:\\Program Files (x86)\\chromedriver.exe");
		WebDriver web = new ChromeDriver();
		web.get("http://secondhandbookstore.pythonanywhere.com/");
		

		  JavascriptExecutor  js = (JavascriptExecutor) web;
		  web.manage().window().maximize();
		
//		  web.manage().timeouts().implicitlyWait(50, TimeUnit.SECONDS);
		  
		   web.findElement(By.linkText("About")).click();
		   Thread.sleep(100);
		  
		  web.findElement(By.linkText("Home")).click();
		  Thread.sleep(1000);
		  //web.manage().wait(1);
		  
		
		   
		   web.findElement(By.linkText("Contact")).click();
		   Thread.sleep(1000);
		
		 //web.quit();
			
		
	}

}
