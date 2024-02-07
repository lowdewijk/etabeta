import {useMutation, useQuery, useQueryClient} from 'react-query';
import {toast} from 'react-toastify';

import {
  createSession as clientCreateSession,
  deleteSession as clientDeleteSession,
  listSessions,
} from '../api_client/sessions';

export const useListSessions = () => {
  return useQuery('sessions', () => listSessions());
};

export const useCreateSession = () => {
  const client = useQueryClient();

  return useMutation(clientCreateSession, {
    onError: (error: Error) => {
      toast.error('Error creating session: ' + error.message);
    },
    onSuccess: async () => {
      await client.invalidateQueries({queryKey: ['sessions']});
    },
  });
};

export const useDeleteSession = () => {
  const client = useQueryClient();

  return useMutation(clientDeleteSession, {
    onError: (error: Error) => {
      toast.error('Error deleting session: ' + error.message);
    },
    onSuccess: async () => {
      await client.invalidateQueries({queryKey: ['sessions']});
    },
  });
};
