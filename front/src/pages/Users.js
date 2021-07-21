import React,{useState,useEffect} from "react";
import './Users.css';
import {useNavigate} from 'react-router-dom';


let ws=null;
function Users(){
    const navigate = useNavigate();
    const [data,setData]=useState(null);
    const [loading,setLoading]=useState(false);
    const [error,setError]=useState(null);
    
   

    let selectUserToPlay=(user)=>{
        fetch(`http://localhost:3001/game`,{
            method: "POST",
            body: JSON.stringify({user_a: localStorage["username"],user_b:user}),
            headers: {"Content-type": "application/json; charset=UTF-8"}
        })
        .then((data)=>data.json())
        .then((data)=>{
            localStorage["id"]=data.id;
            localStorage["user_a"]=data.user_a;
            localStorage["user_b"]=data.user_b;
            localStorage["board"]=data.board;
            if(localStorage["username"]==data.user_a)localStorage["mark"]=1;
            else localStorage["mark"]=2;
            navigate("/game");
        });
    };
    
    useEffect(()=>{
        setLoading(true);
        fetch(`http://localhost:3001/users`)
        .then((data)=>data.json())
        .then(setData)
        .then(()=>setLoading(false))
        .catch(setError);
        
        ws = new WebSocket("ws://localhost:3002");

        ws.onmessage = function (e) {
            let game=JSON.parse(e.data);
            if(game.users){
                setData(game.users);
            }
        };
    }, []);
    
    if(loading)return <h1>Loading...</h1>
    else if(error)return <pre>{JSON.stringify(error, null, 2)}</pre>
    else if(data){
        console.log(data);
        // data=data.filter(x => x.user != localStorage["username"])
        let temp=[];
        for(var i=0;i<data.length;i++){
            if(data[i].user!=localStorage["username"])
                temp.push(data[i]);
        }
        if(temp.length==0){
            return (<h3 className="text-center text-white pt-3">There are no users to play, wait for it (or open a private window and play with yourself).</h3>)
        }else{
            return (
            <>
                <h3 className="text-center text-white pt-3">Select user to play with</h3>
                <div id="user-list">
                    {temp.map((user,i)=><div onClick={()=>selectUserToPlay(user.user)} key={i}>{user.user}</div>)}
                </div>
            </>)
        }
    }else{
        return (<div>no user available</div>)
    }
}



export default Users;
