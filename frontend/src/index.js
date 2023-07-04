import React from 'react';
import { BrowserRouter, Routes, Route } from "react-router-dom";
import ReactDOM from 'react-dom/client';
import './index.css';
import App from './App';
import Home from './Home';
// import Mongo from './Mongo'

const root = ReactDOM.createRoot(document.getElementById('root'));
root.render(
  <BrowserRouter>
    <Routes>
    <Route path="/">
      <Route index element={<Home />}/>
      {/* <Route path='mongo' element={<Mongo />}/> */}
      </Route>
    </Routes>
  </BrowserRouter>
  /* <React.StrictMode>
    <Home />
  </React.StrictMode> */
);

// If you want to start measuring performance in your app, pass a function
// to log results (for example: reportWebVitals(console.log))
// or send to an analytics endpoint. Learn more: https://bit.ly/CRA-vitals
