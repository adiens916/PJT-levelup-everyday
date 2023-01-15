import axios from 'axios';
import { useEffect, useState } from 'react';
import { getHabits } from '../api/crudApi';
import { HabitType } from '../types';

export default function useHabitList() {
  const [habits, setHabits] = useState<HabitType[] | null>(null);
  const [loading, setLoading] = useState(true);
  const [isError, setIsError] = useState(false);
  const [errorCode, setErrorCode] = useState(0);

  const fetchHabits = async () => {
    try {
      const habits = await getHabits();
      setHabits(habits);
    } catch (error) {
      if (axios.isAxiosError(error) && error.response) {
        setIsError(true);
        setErrorCode(error.response.status);
      }
    } finally {
      setLoading(false);
    }
  };

  useEffect(() => {
    fetchHabits();
  }, []);

  return { habits, loading, isError, errorCode };
}
