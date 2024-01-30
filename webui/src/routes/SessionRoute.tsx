import {FC} from 'react';
import {useParams} from 'react-router-dom';

import {SessionPage} from '../pages/Session/SessionPage';

export const SessionRoute: FC = () => {
  const {sessionId} = useParams();
  if (!sessionId) {
    throw new TypeError(`Missing session ID.`);
  }

  return <SessionPage sessionID={sessionId} />;
};
