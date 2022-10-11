import axios from 'axios';
import { useEffect, useState } from 'react';
import { extractFields, getHabits } from '../../api/api';
import { HabitType } from '../../api/types';

export default function useHabitList() {
  const [habits, setHabits] = useState<HabitType[]>([]);
  const [loading, setLoading] = useState(true);
  const [isError, setIsError] = useState(false);
  const [errorCode, setErrorCode] = useState(0);

  const fetchHabits = async () => {
    try {
      const response = await getHabits();
      const convertedHabits = extractFields(response.data);
      setHabits(convertedHabits);
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
