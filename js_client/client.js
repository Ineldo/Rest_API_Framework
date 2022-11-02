const loginForm = document.getElementById('login-form');
const searchForm = document.getElementById('search-form');
const contentContainer = document.getElementById('content-container');
const baseEndpoint= "http://127.0.0.1:8000/api/"
if(loginForm){
    //handle this login form
    loginForm.addEventListener('submit', handleLogin)
}
if(searchForm){
    //handle this search form
    searchForm.addEventListener('submit', handleSearch)
}

function handleLogin(event){
    event.preventDefault();
    const loginEndpoint = `${baseEndpoint}token/`
    let loginFormData= new FormData(loginForm)//FormData is a built-in js class
    let loginObjectData= Object.fromEntries(loginFormData)
    let bodyStr= JSON.stringify(loginObjectData)//with this the API will know how to handle the info passed
    console.log(loginObjectData, bodyStr)
    const options = {
        method: "POST",
        headers:{
            "Content-Type": "application/json"
        },
        body: bodyStr
    }
    fetch(loginEndpoint, options)
    .then(response => {
        return response.json()
    })
    .then(authData=>{
        handleAuthData(authData, getProductList)
    })
    .catch(err => {
        console.log('err',err)
    })
}

function handleSearch(event){
    event.preventDefault();
   
    let formData= new FormData(searchForm)//FormData is a built-in js class
    let data= Object.fromEntries(formData)
    let searchParams= new URLSearchParams(data)
    const endpoint = `${baseEndpoint}search/?${searchParams}`
    const headers = {
        "Content-Type": "application/json",
    }
    const authToken= localStorage.getItem('access') 
    if (authToken){
        headers['Authorization'] =`Bearer ${authToken}`
    }
    const options = {
        method: "GET",
        headers:{
           headers:headers
        },
      
    }
    fetch(endpoint, options)
    .then(response => {
        return response.json()
    })
    .then(data=>{
        console.log(data.hits)
        writeToContainer(data)
    })
    .catch(err => {
        console.log('err',err)
    })
}


function writeToContainer(data) {
    if(contentContainer){
        contentContainer.innerHTML="<pre>"+ JSON.stringify(data, null, 4) +"</pre>"
    }

}

function handleAuthData(authData, callback) {
    localStorage.setItem('access', authData.access)

    localStorage.setItem('refresh', authData.refresh)
    if(callback){
        callback()
    }


}
function getFetchOptions(method, body){
    return {
        method: method === null ? 'GET' : method,
        headers:{
            "Content-type": "application/json",
            "Authorization":`Bearer ${localStorage.getItem('access')}`
        },
        body: body ? body : null
    }
}

function isTokenValid(jsonData){
    if(jsonData.code && jsonData.code==="token_not_valid"){
      //  alert("you gotta login again")
    }

}
function getProductList(){
    const endpoint = `${baseEndpoint}products/`
    const options = getFetchOptions()
    fetch(endpoint, options)
    .then(response =>{ 
        return response.json()
    })
    .then(data=>{
        const validToken=isTokenValid(data)
        if(validToken){
           writeToContainer(data)

        }
    })
}
getProductList()

const searchClient = algoliasearch('MJL35Y9IM0', 'fb242116cc8ba2e6c2a85bd72b0fda73');

const search = instantsearch({
  indexName: 'ineldo_Products',
  searchClient,
});

search.addWidgets([
  instantsearch.widgets.searchBox({
    container: '#searchbox',
  }),

  instantsearch.widgets.refinementList({
    container: '#user-list',
    attribute:'user'
  }),

  instantsearch.widgets.hits({
    container: '#hits',
    templates: {
       item:`<div>{{title}}<p>\${{price}}</p><p>{{body}}</p><p>{{user}}</p></div>` 
    }
  })
]);

search.start();
