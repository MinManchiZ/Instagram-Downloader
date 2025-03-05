
from selenium import webdriver
from selenium.webdriver.edge.service import Service
from selenium.webdriver.edge.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException
import os
import time
import urllib.request
import logging
class InstagramDownloader:
    def __init__(self, driver_path, download_path="downloads"):
      
        self.download_path = download_path
        self.driver_path = driver_path
        self.setup_logging()
        self.setup_driver()
        self.ensure_download_directory()

    def setup_logging(self):
       
        logging.basicConfig(
            level=logging.INFO,
            format='%(asctime)s - %(levelname)s - %(message)s'
        )
        self.logger = logging.getLogger(__name__)

    def setup_driver(self):
        
        try:
            options = Options()
            options.add_argument("--start-maximized")
            options.add_experimental_option("excludeSwitches", ["enable-logging"])
            
            service = Service(self.driver_path)
            self.driver = webdriver.Edge(service=service, options=options)
            self.wait = WebDriverWait(self.driver, 10)
            self.logger.info("WebDriver初始化成功")
        except Exception as e:
            self.logger.error(f"WebDriver初始化失败: {e}")
            raise

    def ensure_download_directory(self):
      
        if not os.path.exists(self.download_path):
            os.makedirs(self.download_path)
            self.logger.info(f"创建下载目录: {self.download_path}")

    def wait_and_handle_popups(self):
       
        try:
        
            cookie_button = self.wait.until(
                EC.presence_of_element_located((
                    By.XPATH,
                    "//button[contains(@class, '_a9--')]"
                ))
            )
            cookie_button.click()
            self.logger.info("已处理Cookie弹窗")
            time.sleep(2)

            try:
                login_popup = self.wait.until(
                    EC.element_to_be_clickable((
                        By.XPATH,
                        "//div[contains(@class, '_ab8w')]//div[@role='button']"
                    ))
                )
                login_popup.click()
                self.logger.info("已处理登录弹窗")
            except TimeoutException:
                self.logger.info("未检测到登录弹窗")

        except Exception as e:
            self.logger.warning(f"处理弹窗时出现异常: {e}")

def download_media_files(self):
 
    try:
     
        images = self.driver.find_elements(
            By.XPATH,
            "//div[contains(@class, '_aagw')]/preceding-sibling::img[contains(@class, 'x5yr21d')]"
        )
        
        if not images:
            self.logger.info("当前页面未找到符合条件的图片")
            return False

        self.logger.info(f"找到 {len(images)} 张图片")
        downloaded = False
        
        for idx, img in enumerate(images, 1):
            try:
                src = img.get_attribute('src')
                if not src or not any(token in src for token in ['scontent', '/t51.2885-15/']):
                    continue

                img_id = src.split('?')[0].split('/')[-1].split('_')[0]
                
                
                srcset = img.get_attribute('srcset')
                if srcset:
                    urls = dict(
                        url.strip().split(' ')
                        for url in srcset.split(',')
                        if url.strip()
                    )
                    max_width = max(int(w.replace('w', '')) for w in urls.values())
                    best_url = [url for url, width in urls.items() 
                              if width == f'{max_width}w'][0]
                    
                    filename = os.path.join(
                        self.download_path,
                        f"instagram_{img_id}.jpg"
                    )
                    
                    if not os.path.exists(filename):
                        urllib.request.urlretrieve(best_url, filename)
                        self.logger.info(f"已下载高清图片: {filename}")
                        downloaded = True
                    else:
                        self.logger.info(f"图片已存在，跳过: {filename}")
                
            except Exception as e:
                self.logger.error(f"处理第 {idx} 张图片时出错: {e}")
                continue

        
        videos = self.driver.find_elements(
            By.XPATH,
            "//div[contains(@class, '_aagw')]/preceding-sibling::video"
        )
        
        for idx, video in enumerate(videos, 1):
            try:
                src = video.get_attribute('src')
                if not src:
                    continue

                video_id = src.split('?')[0].split('/')[-1].split('_')[0]
                filename = os.path.join(
                    self.download_path,
                    f"instagram_{video_id}.mp4"
                )
                
                if not os.path.exists(filename):
                    urllib.request.urlretrieve(src, filename)
                    self.logger.info(f"已下载视频: {filename}")
                    downloaded = True
                else:
                    self.logger.info(f"视频已存在，跳过: {filename}")
                    
            except Exception as e:
                self.logger.error(f"处理第 {idx} 个视频时出错: {e}")
                continue

        return downloaded

    except Exception as e:
        self.logger.error(f"下载媒体文件失败: {e}")
        return False

    def process_url(self, url):

        try:
            self.logger.info(f"正在访问: {url}")
            self.driver.get(url)
        
    
            self.wait.until(EC.presence_of_element_located((By.TAG_NAME, "body")))
            self.wait_and_handle_popups()
     
            while True:
                self.download_media_files()
            
                try:
               
                    next_button = self.driver.find_element(
                        By.XPATH,
                        "//button[@aria-label='下一步' and contains(@class, '_afxw')]"
                    )
                
                    if next_button.is_enabled():
                        self.logger.info("点击下一步按钮")
                        next_button.click()
                  
                        time.sleep(2)
                    else:
                        self.logger.info("已到达最后一张图片")
                        break
                    
                except Exception as e:
                    self.logger.info("未找到下一步按钮，可能只有一张图片")
                    break
                
        except Exception as e:
            self.logger.error(f"处理URL失败: {e}")

    def close(self):
       
        try:
            self.driver.quit()
            self.logger.info("浏览器已关闭")
        except Exception as e:
            self.logger.error(f"关闭浏览器失败: {e}")

def download_media_files(self):
   
    try:
      
        images = self.driver.find_elements(
            By.XPATH,
            "//div[contains(@class, '_aagv')]//img[contains(@class, 'x5yr21d') and contains(@class, 'xu96u03')]"
        )
        
        if not images:
            self.logger.info("当前页面未找到符合条件的图片")
            return False

        self.logger.info(f"找到 {len(images)} 张图片")
        downloaded = False
        
        for idx, img in enumerate(images, 1):
            try:
                src = img.get_attribute('src')
                if not src or not any(token in src for token in ['scontent', '/t51.2885-15/']):
                    continue

              
                url_parts = src.split('?')[0].split('/')
                img_id = url_parts[-1] if url_parts else str(int(time.time()))
              
                srcset = img.get_attribute('srcset')
                if srcset:
                    urls = dict(
                        url.strip().split(' ')
                        for url in srcset.split(',')
                        if url.strip()
                    )
                    max_width = max(int(w.replace('w', '')) for w in urls.values())
                    best_url = [url for url, width in urls.items() 
                              if width == f'{max_width}w'][0]
                    
                    filename = os.path.join(
                        self.download_path,
                        f"instagram_{img_id}.jpg"
                    )
                    
                    if not os.path.exists(filename):
                        urllib.request.urlretrieve(best_url, filename)
                        self.logger.info(f"已下载高清图片: {filename}")
                        downloaded = True
                    else:
                        self.logger.info(f"图片已存在，跳过: {filename}")
                
            except Exception as e:
                self.logger.error(f"处理第 {idx} 张图片时出错: {e}")
                continue

        
        videos = self.driver.find_elements(
            By.XPATH,
            "//div[contains(@class, '_aagv')]//video"
        )
        
        for idx, video in enumerate(videos, 1):
            try:
                src = video.get_attribute('src')
                if not src:
                    continue

                
                url_parts = src.split('?')[0].split('/')
                video_id = url_parts[-1] if url_parts else str(int(time.time()))
                
                filename = os.path.join(
                    self.download_path,
                    f"instagram_{video_id}.mp4"
                )
                
                if not os.path.exists(filename):
                    urllib.request.urlretrieve(src, filename)
                    self.logger.info(f"已下载视频: {filename}")
                    downloaded = True
                else:
                    self.logger.info(f"视频已存在，跳过: {filename}")
                    
            except Exception as e:
                self.logger.error(f"处理第 {idx} 个视频时出错: {e}")
                continue

        return downloaded

    except Exception as e:
        self.logger.error(f"下载媒体文件失败: {e}")
        return False

def process_url(self, url):
    
    try:
        self.logger.info(f"正在访问: {url}")
        self.driver.get(url)
        
        
        self.wait.until(EC.presence_of_element_located((By.TAG_NAME, "body")))
        self.wait_and_handle_popups()
        
        
        processed_count = 0
        while True:
            
            if self.download_media_files():
                processed_count += 1
            
            try:
               
                next_button = self.driver.find_element(
                    By.XPATH,
                    "//button[@aria-label='下一步' and contains(@class, '_afxw')]"
                )
                
                if next_button.is_enabled():
                    self.logger.info(f"已处理 {processed_count} 个项目，点击下一步")
                    next_button.click()
                    
                    time.sleep(2)
                    self.wait.until(EC.staleness_of(next_button))
                else:
                    self.logger.info("已到达最后一项")
                    break
                    
            except Exception as e:
                self.logger.info("未找到下一步按钮，可能已处理完所有内容")
                break
                
        self.logger.info(f"共处理了 {processed_count} 个项目")
            
    except Exception as e:
        self.logger.error(f"处理URL失败: {e}")

def main():
    DRIVER_PATH = r"G:\edgedriver_win64\msedgedriver.exe"
    
    try:
        downloader = InstagramDownloader(DRIVER_PATH)
        
        while True:
            url = input("\n请输入Instagram链接 (输入'q'退出): ").strip()
            
            if url.lower() == 'q':
                break
                
            if 'instagram.com' not in url:
                print("错误: 请输入有效的Instagram链接!")
                continue
                
            downloader.process_url(url)
            
    except KeyboardInterrupt:
        print("\n程序已被用户中断")
    except Exception as e:
        print(f"程序执行出错: {e}")
    finally:
        downloader.close()

if __name__ == "__main__":
    main()
    
    
    