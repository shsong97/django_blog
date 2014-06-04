var baseUrl='http://127.0.0.1:8000/timeline';
var username;
var password;
var loginstring;

var doJoin=function() {
    var name=$("#name").val();
    username=$("#username").val();
    password=$("#password").val();
    $.ajax({
        type:'post',
        url:baseUrl+'api/user/create/',
        data:{
            username:username,
            name:name,
            password:password
        },
        success:function() {
            alert("OK");
            location.href="login.html";
        },
        error:function(msg) {
            alert("Error!");
        },
    });
}

var goAdmin=function() {
    location.href=baseUrl+"admin/";
}

var doLogin=function() {
    username=$('#username').val();
    password=$('#password').val();
    loginstring="Basic "+Base64.encode(username+":"+password);
    
    $.ajax({
        type:'get',
        url:baseUrl+'api/login/',
        beforeSend:function(req){
            req.setRequestHeader('Authorization',loginstring);
        },
        success:function(data) {
            alert("Login success");
            setLoginString();
            window.location="timeline.html";
        },
        error:function(){
            alert("Fail to get data!");
        },
        
    });
}

function setCookie(name, value, day) {
    var expire=new Date();
    expire.setDate(expire.getDate()+day);
    cookies=name+'='+escape(value)+';path=/';
    if(typeof day!= 'undefined')
        cookies+=';expires='+expire.toGMTString()+";";
    document.cookie=cookies;
}

function getCookie(name) {
    name=name+'=';
    var cookieData=document.cookie;
    var start=cookieData.indexOf(name);
    var value='';
    if (start != -1) {
        start+=name.length;
        var end=cookieData.indexOf(';',start);
        if(end == -1)
            end=cookieData.length;
        value=cookieData.substring(start,end);
    }
    return unescape(value);
}

function getLoginString() {
    loginstring=getCookie("loginstring");
    username=getCookie("username");
}

function setLoginString() {
    setCookie("loginstring",loginstring,1);
    setCookie("username",username,1);
}

function resetLoginString() {
    setCookie("loginstring","","-1");
    setCookie("username","","-1");
}

function checkLoginString() {
    if(loginstring=="") {
        history.back();
    }
}