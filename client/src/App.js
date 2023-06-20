import React, { useState } from 'react';
import { Routes, Route } from "react-router-dom";
import "bootstrap/dist/css/bootstrap.css";
import './stylesheets/styles.css';
import Home from './components/pages/Home.js'
import SetsPage from './components/pages/SetsPage.js'
import SetDetailsPage from './components/pages/SetDetailsPage.js'
import AllCardsPage from './components/pages/AllCardsPage.js'
import Header from './components/Header.js'
import Footer from './components/Footer.js'

function App() {

  // Dark Mode
  const [darkMode, setDarkMode] = useState(false)

  return (
    <div className={ `App ${darkMode ? 'DarkMode' : 'LightMode'}`}>
      <Header darkMode={darkMode} updateDarkMode={() => setDarkMode((prev) => !prev)}/>
      <Routes>
        <Route path='/' element={<Home />} />
        <Route path='/sets' element={<SetsPage />} />
        <Route path='/cards' element={<AllCardsPage />} />
        <Route path='/sets/:id' element={<SetDetailsPage />} />
      </Routes>
      <Footer/>
    </div>
  );
}

export default App;
