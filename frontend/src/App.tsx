import React from 'react';
import { BrowserRouter, Routes, Route } from 'react-router-dom';
import { RecoilRoot } from 'recoil';

import HabitList from './components/HabitList/HabitList';
import HabitCreate from './components/HabitCreate/HabitCreate';
import HabitTimer from './components/HabitTimer/HabitTimer';
import SignUp from './components/SignUp/SignUp';
import Login from './components/Login/Login';
import NavBar from './components/NavBar/NavBar';

function App() {
  return (
    <RecoilRoot>
      <BrowserRouter>
        <Routes>
          <Route element={<NavBar />}>
            <Route path="/" element={<HabitList />} />
            <Route path="/create" element={<HabitCreate />} />
            <Route path="/timer" element={<HabitTimer />} />
            <Route path="/signup" element={<SignUp />} />
            <Route path="/login" element={<Login />} />
          </Route>
        </Routes>
      </BrowserRouter>
    </RecoilRoot>
  );
}

export default App;
