import requests
import random
import string
import time
import argparse
import threading
import concurrent.futures
import sys
from datetime import datetime

def random_string(length=8, include_symbols=False):
    chars = string.ascii_letters + string.digits
    if include_symbols:
        # 添加更多特殊符号，但避免可能导致问题的符号
        symbols = "._-+=#$!%^&*"
        chars += symbols
    return ''.join(random.choice(chars) for _ in range(length))

def generate_email_prefix(length):
    # 确保邮箱前缀以字母开头
    prefix = random.choice(string.ascii_letters)
    # 剩余部分使用字母和数字
    remaining_length = length - 1
    prefix += ''.join(random.choice(string.ascii_letters + string.digits) for _ in range(remaining_length))
    return prefix

def generate_password(length=32):
    # 定义字符集
    lowercase = string.ascii_lowercase
    uppercase = string.ascii_uppercase
    digits = string.digits
    symbols = "!@#$%^&*()_+-=[]{}|;:,.<>?~"
    
    # 确保密码至少包含每种字符
    password = [
        random.choice(lowercase),      # 至少一个小写字母
        random.choice(uppercase),      # 至少一个大写字母
        random.choice(digits),         # 至少一个数字
        random.choice(symbols),        # 至少一个特殊符号
        random.choice(symbols),        # 再加一个特殊符号
        random.choice(uppercase),      # 再加一个大写字母
        random.choice(lowercase),      # 再加一个小写字母
        random.choice(digits)          # 再加一个数字
    ]
    
    # 生成剩余长度的随机字符
    remaining_length = length - len(password)
    all_chars = lowercase + uppercase + digits + symbols
    password.extend(random.choice(all_chars) for _ in range(remaining_length))
    
    # 打乱密码字符顺序
    random.shuffle(password)
    return ''.join(password)

def generate_username(length):
    # 确保用户名以字母开头
    username = random.choice(string.ascii_letters)
    # 剩余部分可以是字母或数字
    remaining_length = length - 1
    username += ''.join(random.choice(string.ascii_letters + string.digits) for _ in range(remaining_length))
    return username

# 随机生成的50个 User-Agent 字符串列表
user_agents = [
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/95.0.4638.69 Safari/537.36",
    "Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/94.0.4606.81 Safari/537.36",
    "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/15.0 Safari/605.1.15",
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:93.0) Gecko/20100101 Firefox/93.0",
    "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/96.0.4664.45 Safari/537.36",
    "Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/92.0.4515.107 Safari/537.36",
    "Mozilla/5.0 (Macintosh; Intel Mac OS X 11_2_3) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.114 Safari/537.36",
    "Mozilla/5.0 (Windows NT 6.3; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/90.0.4430.212 Safari/537.36",
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Edge/95.0.1020.44",
    "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/89.0.4389.82 Safari/537.36",
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/88.0.4324.190 Safari/537.36",
    "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_14_6) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/87.0.4280.141 Safari/537.36",
    "Mozilla/5.0 (Linux; Android 10; SM-G973F) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/86.0.4240.198 Mobile Safari/537.36",
    "Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/85.0.4183.121 Safari/537.36",
    "Mozilla/5.0 (iPhone; CPU iPhone OS 14_0 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/14.0 Mobile/15A372 Safari/604.1",
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Firefox/84.0",
    "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_6) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/83.0.4103.116 Safari/537.36",
    "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/82.0.4085.131 Safari/537.36",
    "Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/81.0.4044.138 Safari/537.36",
    "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_14_0) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/13.0 Safari/605.1.15",
    "Mozilla/5.0 (Windows NT 10.0; WOW64; rv:45.0) Gecko/20100101 Firefox/45.0",
    "Mozilla/5.0 (Windows NT 6.1; WOW64; rv:40.0) Gecko/20100101 Firefox/40.1",
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/80.0.3987.132 Safari/537.36",
    "Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:78.0) Gecko/20100101 Firefox/78.0",
    "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_12_6) AppleWebKit/603.3.8 (KHTML, like Gecko) Version/10.1.2 Safari/603.3.8",
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/79.0.3945.130 Safari/537.36",
    "Mozilla/5.0 (Linux; Android 9; SM-A505FN) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/78.0.3904.108 Mobile Safari/537.36",
    "Mozilla/5.0 (iPhone; CPU iPhone OS 13_5 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/13.1.1 Mobile/15E148 Safari/604.1",
    "Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Firefox/75.0",
    "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_13_6) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/76.0.3809.132 Safari/537.36",
    "Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Firefox/74.0",
    "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/73.0.3683.86 Safari/537.36",
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/72.0.3626.121 Safari/537.36",
    "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_11_6) AppleWebKit/604.5.6 (KHTML, like Gecko) Version/11.1.2 Safari/604.5.6",
    "Mozilla/5.0 (Windows NT 6.1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/71.0.3578.98 Safari/537.36",
    "Mozilla/5.0 (iPhone; CPU iPhone OS 12_0 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/12.0 Mobile/15A372 Safari/604.1",
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:68.0) Gecko/20100101 Firefox/68.0",
    "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_10_5) AppleWebKit/600.8.9 (KHTML, like Gecko) Version/8.0.8 Safari/600.8.9",
    "Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:67.0) Gecko/20100101 Firefox/67.0",
    "Mozilla/5.0 (Windows NT 6.3; Trident/7.0; rv:11.0) like Gecko",
    "Mozilla/5.0 (Windows NT 10.0; WOW64; rv:65.0) Gecko/20100101 Firefox/65.0",
    "Mozilla/5.0 (iPad; CPU OS 12_2 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/12.1 Mobile/15E148 Safari/604.1",
    "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_9_5) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/64.0.3282.186 Safari/537.36",
    "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/63.0.3239.132 Safari/537.36",
    "Mozilla/5.0 (Windows NT 6.1; WOW64; rv:60.0) Gecko/20100101 Firefox/60.0",
    "Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/62.0.3202.94 Safari/537.36",
    "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_8_5) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/61.0.3163.100 Safari/537.36",
    "Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/60.0.3112.113 Safari/537.36",
    "Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:55.0) Gecko/20100101 Firefox/55.0",
    "Mozilla/5.0 (Windows NT 6.2; Trident/7.0; rv:11.0) like Gecko",
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/54.0.2840.99 Safari/537.36",
    "Mozilla/5.0 (iPhone; CPU iPhone OS 10_3 like Mac OS X) AppleWebKit/602.1.50 (KHTML, like Gecko) Version/10.0 Mobile/14E5239e Safari/602.1",
    "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_7_5) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/49.0.2623.112 Safari/537.36",
    "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/48.0.2564.116 Safari/537.36"
]

def register_account(base_url):
    # 随机选择邮箱后缀列表
    email_suffixes = [
    "hotmail.com", "gmail.com", "qq.com", "163.com", "126.com", "139.com", "aliyun.com", "mail.com",
    "yahoo.com", "outlook.com", "icloud.com", "aol.com", "zoho.com", "yandex.com", "proton.me", "protonmail.com",
    "sina.com", "sohu.com", "msn.com", "live.com", "mac.com", "me.com", "fastmail.com", "rediff.com",
    "gmx.com", "mail.ru", "comcast.net", "verizon.net", "bellsouth.net", "earthlink.net", "cox.net", "att.net",
    "btinternet.com", "sky.com", "talktalk.net", "virginmedia.com", "t-online.de", "web.de", "laposte.net", "wanadoo.fr",
    "orange.fr", "free.fr", "bluewin.ch", "seznam.cz", "tiscali.it", "libero.it", "tin.it", "inwind.it",
    "iol.it", "terra.com.br", "bol.com.br", "uol.com.br", "ig.com.br", "r7.com", "globo.com", "outlook.in",
    "rediffmail.com", "indiatimes.com", "bigpond.com", "optusnet.com.au", "xtra.co.nz", "telstra.com", "vodafone.com.au", "hotmail.co.uk",
    "yahoo.co.uk", "outlook.co.uk", "live.co.uk", "gmail.co.uk", "mail.com", "mail.cn", "mail.hk", "mail.tw",
    "hinet.net", "seed.net.tw", "pchome.com.tw", "myway.com", "excite.com", "rocketmail.com", "netscape.net", "usa.net",
    "email.com", "iname.com", "care2.com", "bigfoot.com", "clara.net", "netzero.net", "juno.com", "peoplepc.com",
    "cs.com", "swbell.net", "uswest.net", "midco.net", "frontier.com", "charter.net", "knology.net", "embarqmail.com",
    "centurylink.net", "netcabo.pt", "iol.pt", "sapo.pt", "click21.com.br", "ig.com", "265.com", "xinhuanet.com"
]

    suffix = random.choice(email_suffixes)
    
    # 生成邮箱前缀（20-25位，只包含字母和数字）
    email_prefix = generate_email_prefix(random.randint(20, 25))
    email = f"{email_prefix}@{suffix}"
    username = generate_username(random.randint(20, 25))  # 用户名20-25位，只包含字母和数字
    password = generate_password(random.randint(32, 40))  # 生成32-40位的密码
    
    # 构建表单数据
    payload = {
        "email": email,
        "username": username,
        "password": password,
        "confirm_password": password,
        "agree_terms": "on",
        "register": ""
    }
    
    # 设置完整的请求头
    headers = {
        "accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.7",
        "accept-language": "zh-CN,zh;q=0.9,en;q=0.8,en-CN;q=0.7",
        "cache-control": "no-cache",
        "content-type": "application/x-www-form-urlencoded",
        "origin": "https://www.xzphotos.cn",
        "pragma": "no-cache",
        "priority": "u=0, i",
        "referer": "https://www.xzphotos.cn/register.php",
        "sec-ch-ua": '"Chromium";v="136", "Google Chrome";v="136", "Not.A/Brand";v="99"',
        "sec-ch-ua-mobile": "?0",
        "sec-ch-ua-platform": '"Windows"',
        "sec-fetch-dest": "document",
        "sec-fetch-mode": "navigate",
        "sec-fetch-site": "same-origin",
        "sec-fetch-user": "?1",
        "upgrade-insecure-requests": "1",
        "user-agent": random.choice(user_agents)  # 使用随机User-Agent
    }
    
    try:
        # 创建session来处理cookies
        session = requests.Session()
        
        # 先访问注册页面获取PHPSESSID
        session.get(f"{base_url}/register.php", headers=headers)
        
        # 发送注册请求
        response = session.post(
            f"{base_url}/register.php",
            data=payload,  # 使用data而不是json，因为是form-urlencoded格式
            headers=headers,
            timeout=10,
            allow_redirects=False  # 不自动跟随重定向，这样可以捕获302状态码
        )
        
        if response.status_code == 302:
            print(f"[成功] 注册成功！账号: {username} 邮箱: {email} 密码: {password}")
            # 保存成功的账号
            with open("successful_accounts.txt", "a", encoding="utf-8") as f:
                f.write(f"账号: {username}, 邮箱: {email}, 密码: {password}\n")
            return True
        else:
            print(f"[失败] 注册失败！账号: {username} 邮箱: {email} 状态码: {response.status_code}")
            if response.text:
                print(f"响应内容: {response.text[:200]}...")  # 只打印前200个字符
            return False
    except Exception as e:
        print(f"[错误] 请求异常: {e}")
        return False

def main():
    parser = argparse.ArgumentParser(description="测试注册账号脚本")
    parser.add_argument(
        "--frequency",
        type=float,
        default=0.5,
        help="注册频率（秒），范围：0.3秒到60秒之间"
    )
    parser.add_argument(
        "--count",
        type=int,
        default=1000,
        help="测试注册账号次数"
    )
    parser.add_argument(
        "--threads",
        type=int,
        default=5,
        help="并发线程数量（1-20之间）"
    )
    args = parser.parse_args()
    
    if args.frequency < 0.3 or args.frequency > 60:
        print("注册频率必须在0.3秒到60秒之间")
        return
    
    if args.threads < 1 or args.threads > 20:
        print("线程数量必须在1到20之间")
        return
    
    if args.threads > 10:
        print("警告：线程数量过高可能导致IP被封禁！")
        response = input("是否继续？(y/n): ")
        if response.lower() != 'y':
            return

    base_url = "https://www.xzphotos.cn"
    
    # 创建计数器和锁
    successful_count = 0
    failed_count = 0
    counter_lock = threading.Lock()
    
    def worker():
        nonlocal successful_count, failed_count
        session = requests.Session()  # 每个线程使用独立的session
        
        while True:
            with counter_lock:
                if successful_count + failed_count >= args.count:
                    break
            
            try:
                result = register_account(base_url)
                with counter_lock:
                    if result:
                        successful_count += 1
                    else:
                        failed_count += 1
                    total = successful_count + failed_count
                    print(f"\r进度: {total}/{args.count} (成功: {successful_count}, 失败: {failed_count})", end="")
                
                time.sleep(args.frequency)
            except Exception as e:
                print(f"\n线程异常: {str(e)}")
                with counter_lock:
                    failed_count += 1
    
    print(f"开始注册 - 总数: {args.count}, 频率: {args.frequency}秒, 线程数: {args.threads}")
    print("按Ctrl+C可以随时停止程序")
    
    # 创建线程池
    threads = []
    try:
        for _ in range(args.threads):
            t = threading.Thread(target=worker)
            t.daemon = True  # 设置为守护线程，这样主线程结束时它们会自动结束
            threads.append(t)
            t.start()
        
        # 等待所有线程完成
        for t in threads:
            t.join()
            
        print(f"\n\n注册完成！")
        print(f"总计: {args.count}")
        print(f"成功: {successful_count}")
        print(f"失败: {failed_count}")
        print(f"成功率: {(successful_count/args.count*100):.2f}%")
        
    except KeyboardInterrupt:
        print("\n\n检测到Ctrl+C，正在优雅退出...")
        print("等待当前任务完成...")
        # 等待所有线程完成当前任务
        for t in threads:
            t.join()
        print(f"\n中途停止！")
        print(f"成功: {successful_count}")
        print(f"失败: {failed_count}")
        if successful_count + failed_count > 0:
            print(f"成功率: {(successful_count/(successful_count+failed_count)*100):.2f}%")
        sys.exit(0)

if __name__ == "__main__":
    main()