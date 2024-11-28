"""
同步已收录的主页文件到 GitHub
"""

from dataclasses import dataclass, field, asdict
from typing import Optional, List
import yaml
import os
import sys
import loguru
import hashlib
import httpx

logger = loguru.logger
# 修改默认日志格式
logger.remove()
logger.add(sys.stderr, format="<green>{time:YYYY-MM-DD HH:mm:ss.SSS}</green> | <level>{level: <8}</level> | <level>{message}</level>")

@dataclass
class HomepageInfo:
    source_url: str = field(default="")
    homepage_name: str = field(default="")
    homepage_link: str = field(default="")
    owner: str = field(default="")
    owner_link: str = field(default="")
    description: str = field(default="")


# 初始化主页列表
def read_config():
    homepage_list = []
    if os.path.exists('homepage_list.yaml'):
        with open('homepage_list.yaml', 'r') as f:
            homepage_list = yaml.load(f, Loader=yaml.FullLoader)
            # 解析 HomepageInfo
            homepage_list = [HomepageInfo(**homepage) for homepage in homepage_list]
            return homepage_list
    else:
        with open('homepage_list.yaml', 'w') as f:
            # 写入一个空 HomepageInfo
            empty_homepage = asdict(HomepageInfo())
            yaml.dump([empty_homepage], f)
            return []


def get_md5(content) -> str:
    md5 = hashlib.md5()
    md5.update(content)
    return md5.hexdigest()

def download_homepage_content(homepage: HomepageInfo) -> Optional[bytes]:
    try:
        with httpx.Client(headers={"User-Agent": "PCL2/homepage_collection", "Referer": "homepage_collection.pcl2.server"},) as client:
            response = client.get(homepage.source_url)
            response.history
            if response.status_code == 200:
                return response.content
            else:
                logger.error(f"下载 {homepage.source_url} 失败，状态码 {response.status_code}")
                return None
    except Exception as e:
        logger.error(f"下载 {homepage.source_url} 失败，错误 {e}")

def get_local_homepage_file_hash(homepage: HomepageInfo) -> Optional[str]:
    local_homepage_file_path = os.path.join(public_dir, homepage.homepage_name, "homepage.xaml")
    if os.path.exists(local_homepage_file_path):
        with open(local_homepage_file_path, 'rb') as f:
            return get_md5(f.read())
    else:
        return None

def update_homepage_version(homepage: HomepageInfo, version: str):
    with open(os.path.join(public_dir, homepage.homepage_name, "homepage.xaml.ini"), "w", encoding="UTF-8") as f:
        f.write(version)
    logger.info(f"{homepage.homepage_name} 版本已更新为 {version}")

def sync_homepage(homepage: HomepageInfo):
    if asdict(homepage) == asdict(HomepageInfo()):
        logger.info("跳过空主页")
    else:
        logger.info(f"正在从 {homepage.source_url} 同步 {homepage.homepage_name}")
        if not os.path.exists(os.path.join(public_dir, homepage.homepage_name)):
            os.makedirs(os.path.join(public_dir, homepage.homepage_name))
        local_homepage_file_hash = get_local_homepage_file_hash(homepage)
        latest_content = download_homepage_content(homepage)
        if latest_content:
            latest_homepage_hash = get_md5(latest_content)
            if latest_homepage_hash != local_homepage_file_hash:
                logger.info(f"{homepage.homepage_name} 有更新，开始同步 {local_homepage_file_hash} -> {latest_homepage_hash}")
                with open(os.path.join(public_dir, homepage.homepage_name, "homepage.xaml"), "wb") as f:
                    f.write(latest_content)
                update_homepage_version(homepage, latest_homepage_hash)
                logger.info(f"{homepage.homepage_name} 同步完成")
            else:
                logger.info(f"{homepage.homepage_name} 无更新")
        else:
            logger.error(f"{homepage.homepage_name} 同步失败")
    

if __name__ == "__main__":
    homepage_list = read_config()
    if len(homepage_list) == 0:
        logger.warning("主页列表为空，终止同步")
        sys.exit(1)
    public_dir = "public"
    if not os.path.exists(public_dir):
        os.makedirs(public_dir)
    logger.info(f"开始同步主页文件，共 {len(homepage_list)} 个主页需要同步")
    for homepage in homepage_list:
        sync_homepage(homepage)
    logger.info("同步完成")