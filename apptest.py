import time
import requests

import streamlit as st
from streamlit_lottie import st_lottie
from streamlit_lottie import st_lottie_spinner


def load_lottieurl(url: str):
    r = requests.get(url)
    if r.status_code != 200:
        return None
    return r.json()


lottie_url_hello = "https://assets7.lottiefiles.com/packages/lf20_49rdyysj.json"
lottie_url_download = "https://assets4.lottiefiles.com/private_files/lf30_t26law.json"
lottie_hello = load_lottieurl(lottie_url_hello)
lottie_download = load_lottieurl(lottie_url_download)


st_lottie(lottie_hello, key="hello")

