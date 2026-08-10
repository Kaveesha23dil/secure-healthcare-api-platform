import { useCallback, useEffect, useState } from "react";
export function useAsync<T>(loader: () => Promise<T>) {
  const [data, setData] = useState<T>(),
    [error, setError] = useState<unknown>(),
    [loading, setLoading] = useState(true);
  const reload = useCallback(() => {
    setLoading(true);
    setError(undefined);
    void loader()
      .then(setData)
      .catch(setError)
      .finally(() => setLoading(false));
  }, [loader]);
  useEffect(() => {
    let active = true;
    void loader()
      .then((value) => {
        if (active) setData(value);
      })
      .catch((reason: unknown) => {
        if (active) setError(reason);
      })
      .finally(() => {
        if (active) setLoading(false);
      });
    return () => {
      active = false;
    };
  }, [loader]);
  return { data, error, loading, reload };
}
