import './App.css';
import React from 'react';
import { Route, Routes } from 'react-router-dom';
import Home from './pages/Home.js';
import Login from './pages/Login.js';
import Register from './pages/Register.js';
import NewClass from "./pages/NewClass";
import StartSession from "./pages/StartSession";
import ViewSession from "./pages/ViewSession";

function App() {
	return (
		<>
			<div className="bg-gray-900 min-h-screen">
				<Routes>
					<Route path="/" element={<Home />} />
					<Route path="/login" element={<Login />} />
					<Route path="/register" element={<Register />} />
					<Route path="/newclass" element={<NewClass />} />
					<Route path="/startsession/:id" element={<StartSession />} />
					<Route path="/viewsession/:id" element={<ViewSession />} />
				</Routes>
			</div>
		</>
	);
}

export default App;
