import {Routes, Route} from "react-router-dom";
import Game from "./pages/Game";
import Users from "./pages/Users";
import Login from "./pages/Login";
import Error404 from "./pages/Error";

function AppRouter(){
    return (
        <div>
            <Routes>
                <Route path="/" element={<Login />}></Route>
                <Route path="/users" element={<Users />}></Route>
                <Route path="/game" element={<Game />}></Route>
                <Route path="/*" element={<Error404 />}></Route>
            </Routes>
        </div>
    )
}

export default AppRouter;