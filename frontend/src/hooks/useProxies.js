import { useEffect, useState } from 'react';

const BASE_URL = window.location.origin;

export const useProxies = () => {
  const [proxies, setProxies] = useState([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState(null);

  const fetchProxies = async () => {
    try {
      setLoading(true);
      const response = await fetch(`${BASE_URL}/_rproxy/proxies`, {
        headers: {
          'Accept': 'application/json',
          'Content-Type': 'application/json'
        }
      });
      if (!response.ok) throw new Error('Failed to fetch proxies');
      const data = await response.json();
      setProxies(data);
      setError(null);
    } catch (err) {
      console.error('Error fetching proxies:', err);
      setError(err.message);
    } finally {
      setLoading(false);
    }
  };

  const addProxy = async (proxyData) => {
    const response = await fetch(`${BASE_URL}/_rproxy/proxies`, {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify(proxyData),
    });
    if (!response.ok) throw new Error('Failed to add proxy');
    await fetchProxies();
    return response.json();
  };

  const deleteProxy = async (proxyId) => {
    const response = await fetch(`${BASE_URL}/_rproxy/proxies/${proxyId}`, {
      method: 'DELETE',
    });
    if (!response.ok) throw new Error('Failed to delete proxy');
    await fetchProxies();
  };

  useEffect(() => {
    fetchProxies();
  }, []);

  return {
    proxies,
    loading,
    error,
    addProxy,
    deleteProxy,
    refetch: fetchProxies
  };
};
