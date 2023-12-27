import axios from 'axios';

export type SessionList = Array<{id: string}>;

export const listSessions = async (): Promise<SessionList> => {
  const response = await axios.get<SessionList>(`/api/session/`);
  return response.data;
};

export const createSession = async (sessionID: string) => {
  return axios.post('/api/session', {sessionID});
};

export const deleteSession = async (sessionID: string) => {
  return axios.delete(`/api/session/${sessionID}`);
};
