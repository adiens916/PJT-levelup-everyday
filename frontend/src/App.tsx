import React from 'react';
import { BrowserRouter, Routes, Route } from 'react-router-dom';
import { RecoilRoot } from 'recoil';

import HabitList from './domain/habit/HabitList/HabitList';
import HabitCreate from './domain/habit/HabitCreate/HabitCreate';
import HabitTimer from './domain/habit/HabitTimer/HabitTimer';
import SignUp from './domain/account/SignUp/SignUp';
import Login from './domain/account/Login/Login';
import NavBar from './components/NavBar/NavBar';
import { DailyGraph } from './domain/habit/Graph/Graph';

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
