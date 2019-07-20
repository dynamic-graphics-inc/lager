import React, {useState} from 'react';
import logo from './logo.svg';
import './App.css';

let logs = require('./logs.json')


function App() {
  // socket.emit()



        //{logs.map(e => {return(<p>{e}</p>)})}

  return (
    <div className="App">
        {logs.map(data => {return(
<div><pre>{JSON.stringify(data, null, 2) }</pre></div>
        )})}
    </div>
  );
}

export default App;
