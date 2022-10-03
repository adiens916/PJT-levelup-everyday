import { useEffect, useState } from 'react';
import { extractFields, getHabits } from '../../api/api';
import { HabitType } from '../../api/types';

export default function useHabitList() {
  const [habits, setHabits] = useState<HabitType[]>([]);
  const [loading, setLoading] = useState(true);
  const [isError, setIsError] = useState(false);
  const [errorCode, setErrorCode] = useState(0);

  useEffect(() => {
    getHabits()
      .then((response) => {
        switch (response.status) {
          case 200:
            setHabits(extractFields(response.data));
            break;
          default:
            break;
        }
      })
      .catch((err) => {
        switch (err.response.status) {
          case 401:
            setIsError(true);
            setErrorCode(401);
            break;
          case 403:
            setIsError(true);
            setErrorCode(403);
            break;
          default:
            setIsError(true);
            break;
        }
      });
    setLoading(false);
  }, []);

  return { habits, loading, isError, errorCode };
}
