import os
import requests


def fetch_json(url):
    import requests

    try:
        response = requests.get(url, timeout=10)
        response.raise_for_status()
    except requests.exceptions.RequestException as e:
        # 네트워크 문제나 HTTP 오류 처리
        print("요청 오류 발생:", e)
        return None

    try:
        data = response.json()
    except ValueError as e:
        # JSON 디코딩 오류 처리
        print("JSON 디코딩 오류 발생:", e)
        return None

    return data


def download_file(url, save_path):

    dir_name = os.path.dirname(save_path)
    jar_name = "server.jar"

    if dir_name:  # 디렉터리 경로가 비어있지 않은지 확인
        os.makedirs(dir_name, exist_ok=True)

    try:
        with requests.get(url, stream=True, timeout=10) as response:
            response.raise_for_status()

            print(f"다운로드 경로: {url}")

            with open(f"{save_path}/{jar_name}", "wb") as file:
                for chunk in response.iter_content(chunk_size=8192):
                    if chunk:
                        file.write(chunk)

    except requests.exceptions.RequestException as e:
        print("다운로드 요청 오류 발생:", e)
    except OSError as e:
        print("파일 접근 오류 발생:", e)

    print(f"다운로드 완료.")