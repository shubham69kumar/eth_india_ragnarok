from django.shortcuts import render
import os
from django.shortcuts import render 
import time
import os
from pathlib import Path
import json
import requests

os.environ["UPLOAD_IPFS"] = "true"
os.environ["api_token"] = "1ab148e6-7347-4de2-8cad-fda879a50e0a"
api_token = os.getenv("api_token")


from pathlib import Path
from django.http import HttpResponse


def get_particular_session(user_key, session_key):
    headers = {
        "authorization": "Bearer {}".format(user_key),
    }
    response = requests.get(
        "https://livepeer.studio/api/stream/{}".format(session_key), headers=headers
    )
    print("particular sesiion")
    return (response.json()["name"])


def get_all_session(user_key):
    headers = {
        "authorization": "Bearer {}".format(user_key),
    }

    response = requests.get(
        "https://livepeer.studio/api/stream?streamsonly=1", headers=headers
    )
    # print(response.json())
    session_key = response.json()[0]["id"]
    name_of_session = get_particular_session(user_key,session_key)

    # make a http call here 
def getting_notifications():
    user_key = "0xD7d489A14Ff70931ED879262b7F0429890Ed4FcB"
    response = requests.get(
        "https://backend-staging.epns.io/apis/v1/users/eip155:5:{}/feeds?page=1&spam=false".format(
            user_key
        )
    )
    # replace the integer to get the values of all the api
    print(response.json()["feeds"][0]["payload"]["notification"])



def create_stream():
    headers = {
        "content-type": "application/json",
        "authorization": "Bearer {}".format(api_token),
    }

    json_data = {
        "name": "again_test",
        "profiles": [
            {
                "name": "720p",
                "bitrate": 2000000,
                "fps": 30,
                "width": 1280,
                "height": 720,
            },
            {
                "name": "480p",
                "bitrate": 1000000,
                "fps": 30,
                "width": 854,
                "height": 480,
            },
            {
                "name": "360p",
                "bitrate": 500000,
                "fps": 30,
                "width": 640,
                "height": 360,
            },
        ],
    }

    response = requests.post(
        "https://livepeer.studio/api/stream", headers=headers, json=json_data
    )
    playbaxkId = (response.json()["playbaxkId"])
    stream_id = "https://livepeercdn.studio/hls/{}/index.m3u8".format(playbaxkId)
    #render this to the frontend


def index(request):
    BASE_DIR = Path(__file__).resolve().parent.parent
    print(( str(BASE_DIR )+ '/home/static/'))
    return render(request , 'student_main.html')


def metamask(request):
    return render(request , 'index.html')

def register(request):
    return render(request , 'student_signin.html')

def signup(request):

    return render(request , 'signup.html' )


def student_data(request):
    data = request.POST
    context ={}
    name =  data['fname']
    context['name'] = data['fname']
    context['password']  = data['password']
    context['email'] = data['email']
    metadata_file_name = "./home/ipfs_files/{}".format(name) + ".json"
    print(metadata_file_name)  # newly added line ----
    if Path(metadata_file_name).exists():
        print("{} already found, delete it to overwrite!".format(metadata_file_name))
    else:
        print("Creating Metadata file: " + metadata_file_name)
        with open(metadata_file_name, "w") as file:
            json.dump(context, file)
        if os.getenv("UPLOAD_IPFS") == "true":
            token_uri = str(upload_to_ipfs(metadata_file_name))
    return render(request ,'student_main.html')

def sign_in(request):
    return render(request , 'sig_up.html')



def home_view(request ):
    data = request.POST
    context ={}
    name =  data['fname']
    context['name'] = data['fname']
    context['password']  = data['password']
    context['email'] = data['email']
    metadata_file_name = "./home/ipfs_files/{}".format(name) + ".json"
    print(metadata_file_name)  # newly added line ----
    if Path(metadata_file_name).exists():
        print("{} already found, delete it to overwrite!".format(metadata_file_name))
    else:
        print("Creating Metadata file: " + metadata_file_name)
        with open(metadata_file_name, "w") as file:
            json.dump(context, file)
        if os.getenv("UPLOAD_IPFS") == "true":
            token_uri = str(upload_to_ipfs(metadata_file_name))
    return render(request, "home_page.html", {'name': data['img']})

def upload_to_ipfs(filepath):
    with Path(filepath).open("rb") as fp:
        image_binary = fp.read()
        ipfs_url = (
            os.getenv("IPFS_URL") if os.getenv("IPFS_URL") else "http://localhost:5001"
        )
        response = requests.post(ipfs_url + "/api/v0/add", files={"file": image_binary})
        ipfs_hash = response.json()["Hash"]
        newHash = ipfs_hash
        filename = filepath.split("/")[-1:][0]
        image_uri = "https://ipfs.io/ipfs/{}".format(ipfs_hash)
        print(image_uri)


def stu_auth(request):
    student_data = request.POST
    print(student_data)

    return render(request , 'student_main.html')

def teach_auth(request):
    return render(request , 'sig_up.html')
