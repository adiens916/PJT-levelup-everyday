import React from 'react';
import { BrowserRouter, Routes, Route } from 'react-router-dom';
import { RecoilRoot } from 'recoil';

import HabitList from './components/HabitList/HabitList';
import HabitCreate from './components/HabitCreate/HabitCreate';
import HabitTimer from './components/HabitTimer/HabitTimer';
import SignUp from './domain/account/SignUp/SignUp';
import Login from './domain/account/Login/Login';
import NavBar from './components/NavBar/NavBar';
import { DailyGraph } from './components/Graph/Graph';

function App() {
  return (
    <RecoilRoot>
      <BrowserRouter>
        <Routes>
          <Route element={<NavBar />}>
            <Route path="/" element={<HabitList />} />
            <Route path="/record/:id" element={<DailyGraph />} />
            <Route path="/create" element={<HabitCreate />} />
            <Route path="/timer/:id" element={<HabitTimer />} />
            <Route path="/signup" element={<SignUp />} />
            <Route path="/login" element={<Login />} />
          </Route>
        </Routes>
      </BrowserRouter>
    </RecoilRoot>
  );
}

export default App;
