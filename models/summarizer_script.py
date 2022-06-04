import requests
from transformers import BartForConditionalGeneration, BartTokenizer
from datetime import datetime, timedelta
today = datetime.date(datetime.today() - timedelta(days = 1))
today_string = datetime.strftime(today, '%Y-%m-%d')

def run():
    #Intilizing the BART model 
    model =  BartForConditionalGeneration.from_pretrained("facebook/bart-large-cnn").to('cuda:0')
    #intializing text tokenizer
    tokenizer = BartTokenizer.from_pretrained("facebook/bart-base")
    #obtain the days articles from the api. The date continously change using format and datetime libraries
    d = "http://api:8000/articles/{}".format(today_string)
    req = requests.get(d)

    j_data = req.json()["list"]

    if j_data != {}:
        
        url = []
        articles = []
        count = []
        
        #Putting the json file contents in lists
        for key in j_data:
            url.append(key["url"])
            articles.append(key["text"])
            count.append(key["count"])


    #The following piece of code summarizes the articles
    #NOTE: the model accepts a maximum length of 512 words, so large articles
    #are summarized iterativley

    sums = []

    def summer(articles, nums):
      temp = ''
      num = 0
      count = 0
      for article in articles:
        i = 0
        if nums[num] <= 100:
          sums.append(article)
      
        else:
          while(nums[num] > 10):
              inputs = tokenizer([article[count: count +  512]], max_length = 512, return_tensors="pt").to(model.device)
              summary_ids = model.generate(inputs["input_ids"], num_beams=2, min_length=0, max_length=50).to(model.device)
              temp +=  tokenizer.batch_decode(summary_ids, skip_special_tokens=True, clean_up_tokenization_spaces=False)[0]
              nums[num] -= 512
              count += 512
          count = 0
          sums.append(temp)
          temp = ''
        
        data = {"url" :"", "summary": ""} 
        
        data["url"] = url[num]
        data["summary"] = sums[num]
        num += 1
        send = requests.post('http://api:8000/summary/', json = data)
      return

    if j_data != {}:
        summer(articles, count)

    url = []
    articles = []
    count = []
    sums = []
