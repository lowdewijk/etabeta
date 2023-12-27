import axios from 'axios';

export type SessionList = Array<{id: string}>;

export const listSessions = async (): Promise<SessionList> => {
  const response = await axios.get<SessionList>(
    `http://localhost:8000/api/session/`,
  );
  return response.data;
};

export const createSession = async (sessionID: string) => {
  return axios.post('http://localhost:8000/api/session', {sessionID});
};

export const deleteSession = async (sessionID: string) => {
  return axios.delete(`http://localhost:8000/api/session/${sessionID}`);
};
