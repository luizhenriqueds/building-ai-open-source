"use client";

import { useEffect, useState } from "react";
import { fetchJson } from "@/lib/api";

type ApiState<T> = { data?: T; loading: boolean; error?: string };

export function useApiGet<T>(path: string): ApiState<T> {
  const [state, setState] = useState<ApiState<T>>({ loading: true });

  useEffect(() => {
    const controller = new AbortController();
    setState((previous) => ({ data: previous.data, loading: true }));
    fetchJson<T>(path, controller.signal)
      .then((data) => setState({ data, loading: false }))
      .catch((error: Error) => {
        if (controller.signal.aborted) return;
        setState((previous) => ({
          data: previous.data,
          loading: false,
          error: error.message,
        }));
      });
    return () => controller.abort();
  }, [path]);

  return state;
}
