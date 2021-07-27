import React, {useState} from "react";
import {useNavigate} from 'react-router-dom';

let ws=null;
function loginGame(username,navigate){
    if(username=="bot"){
        alert("you can't take this username");
        return;
    }
    localStorage["username"]=username;
    fetch(`http://localhost:3001/login`,{
        method: "POST",
        body: JSON.stringify({user: username}),
        headers: {"Content-type": "application/json; charset=UTF-8"}
    })
    .then((data)=>data.json())
    .then(()=>{
        navigate("users");
    });
    ws.send(JSON.stringify({"command":"login", "username":username}));
}

function playWithBot(navigate){
    let randomUser="random-"+Math.random();
    localStorage["mark"]=1;
    localStorage["user_a"]=randomUser;
    localStorage["user_b"]="bot";
    localStorage["username"]=randomUser;
    // localStorage["id"]=-1;
    navigate("/game");
}

function Login(){
    if(!ws){
        ws = new WebSocket("ws://localhost:3002");
    }
    const navigate = useNavigate();
    let [username, setUsername]=useState("username");
    return (<>
    <div id="login">
        <h3 className="text-center text-white pt-3">Welcome to Side-Stacker</h3>
        <div className="container">
            <div id="login-row" className="row justify-content-center align-items-center">
                <div id="login-column" className="col-md-6">
                    <div id="login-box" className="col-md-12">
                        <div id="login-form" className="form" action="" method="post">
                            <h3 className="text-center text-info">Login</h3>
                            <img alt="game logo" src="triki.png" width="100" height="100" className="triki-img" />   
                            <div className="form-group">
                                <label for="username" className="text-info">Username:</label><br></br>
                                <input onChange={e => setUsername(e.target.value)} type="text" name="username" id="username" className="form-control" placeholder="any username"></input>
                            </div>
                            <br></br>
                            <div className="form-group">
                                <button className="btn btn-info btn-md white" onClick={()=>loginGame(username,navigate)}>Enter</button>
                                <br/>
                                <br/>
                                <button className="btn btn-info btn-md white" onClick={()=>playWithBot(navigate)}>Play with bot</button>
                            </div>
                        </div>
                    </div>
                </div>
            </div>
        </div>
    </div>
    </>);
}

export default Login;