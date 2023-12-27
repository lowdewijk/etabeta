import {useMutation, useQuery, useQueryClient} from 'react-query';
import {toast} from 'react-toastify';

import {
  createSession as clientCreateSession,
  deleteSession as clientDeleteSession,
  getMessages,
  listSessions,
  Message,
  sendMessage,
} from 'src/api_client/session';

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

export const useSendMessage = (sessionID: string) => {
  const client = useQueryClient();

  return useMutation((message: Message) => sendMessage(sessionID, message), {
    onError: (error: Error) => {
      toast.error('Error sending message: ' + error.message);
    },
    onSuccess: async () => {
      await client.invalidateQueries({queryKey: ['messages']});
    },
  });
};

export const useGetSessionMessages = (sessionID: string) => {
  // poll for new messages every half second
  return useQuery({
    queryKey: ['messages', sessionID],
    queryFn: () => getMessages(sessionID),
    refetchInterval: 500,
  });
};
