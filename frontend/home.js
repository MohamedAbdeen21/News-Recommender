const IP = "10.112.114.17"
var today = new Date();
var dd = String(today.getDate() - 1).padStart(2, "0");
var mm = String(today.getMonth() + 1).padStart(2, "0"); //January is 0!
var yyyy = today.getFullYear();
today = yyyy + "-" + mm + "-" + dd;

function makeid(length) {
  var result = "";
  var characters =
    "ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz0123456789";
  var charactersLength = characters.length;
  const d = new Date();
  var log = [];
  for (var i = 0; i < length; i++) {
    result += characters.charAt(Math.floor(Math.random() * charactersLength));
  }
  return result;
}
  var rand = makeid(30)
  let temp = document.cookie
  let rec = temp.slice(9, temp.length)
  const getDataIfNotAvailable = ()=>{
    fetch(
    `http://${IP}:8000/articles/${today}/`)
      .then((res) => res.json())
      .then((data) => {
        for (var i = 0; i < data.length; i++) {
          var temp = document.querySelector(".article_container").content;
          var copy_temp = document.importNode(temp, true);
          var obj = data[i];

          copy_temp.querySelector(".title").textContent = obj.title;
          copy_temp.querySelector(".summary").textContent = obj.summary;

          copy_temp.querySelector("#ref_title").href = obj.url;
          // console.log(copy_temp.querySelector('#ref_title').href)

          document.getElementById("feed").appendChild(copy_temp);
        }
      })
  }
  const getDataIfAvailable = ()=>{
    fetch(`http://${IP}:8000/${rec}/`)
    .then((res) => res.json())
    .then((data) =>{
      for (var i = 0; i < data.length; i++) {
        var temp = document.querySelector(".article_container").content;
        var copy_temp = document.importNode(temp, true);
        var obj = data[i];

        copy_temp.querySelector(".title").textContent = obj.title;
        copy_temp.querySelector(".summary").textContent = obj.summary;

        copy_temp.querySelector("#ref_title").href = obj.url;
        // console.log(copy_temp.querySelector('#ref_title').href)

        document.getElementById("feed").appendChild(copy_temp);
  }})}

document.addEventListener("DOMContentLoaded", (e)=>{

  setTimeout(loadData, 1000);
const drawer = document.querySelector(".drawer");
const nav = document.querySelector("nav");
const articleCard = document.querySelector("[article]");
const articleFeed = document.querySelector("[feed]");

//const searchin = document.querySelector()
let min = window.innerWidth;

drawer.addEventListener("click", () => {
  nav.classList.add("open-nav");
  nav.classList.remove("close-nav");
});

document.getElementsByClassName("feed")[0].addEventListener("click", (e) => {
  nav.classList.remove("open-nav");
  if (min < 920) {
    nav.classList.add("close-nav");
  }
});

//A function to get today's articles for first time users

if (document.cookie === "") {
  document.cookie = `username = ${rand}`
  fetch(
    `http://${IP}:8000/articles/${today}/`)
      .then((res) => res.json())
      .then((data) => {
        for (var i = 0; i < data.length; i++) {
          var temp = document.querySelector(".article_container").content;
          var copy_temp = document.importNode(temp, true);
          var obj = data[i];

          copy_temp.querySelector(".title").textContent = obj.title;
          copy_temp.querySelector(".summary").textContent = obj.summary;

          copy_temp.querySelector("#ref_title").href = obj.url;
          // console.log(copy_temp.querySelector('#ref_title').href)

          document.getElementById("feed").appendChild(copy_temp);
        }
      })
  ;
}
if(document.cookie !== ''){
  fetch(`http://${IP}:8000/${rec}/`)
    .then((res) => res.json())
    .then((data) =>{
      if(data == ""){
        getDataIfNotAvailable()
      }else{
        getDataIfAvailable()
      }
    })
  }
  
function loadData(){
  //Cookie generation
let ratings = document.querySelectorAll(".article_a_tag");
  for(let i = 0; i < ratings.length; i++){
    let rating = ratings[i];
    rating.addEventListener("click", async () => {
      console.log("clicked")
       fetch(`http://${IP}:8000/rating/`, {
        method: "POST", body: JSON.stringify(
          {"url": rating.href, "rating": 1, 
          "cookieid": rand}), 
          headers:{"Content-Type": "application/json", "Access-Control-Allow-Origin": "*"}})
          .then(data=>data.json()).then(data=>console.log(data))
    })
  }
  
}})

//if cookie there's no cookie, set and display today's articles
//document.cookie = 'fkjasfkjafkja = aaa';
//let req = 'http://10.0.0.12:8000/articles/2022-06-06';
//fetch('http://10.0.0.12:8000/articles/2022-06-06')
//.then(res => res.json())
//.then(data => {
//   users = data.map(user => {
//     const card = articleCard.content.cloneNode(true).children[0];
//   const title = card.querySelector('[title]');
// const summary = card.querySelector('[summary]');

// title.textContent = art.title
//summary.textContent = art.summary

//articleFeed.append(card)
//return { title: user.title, summary: user.summary}

//})})}
