import {FC} from 'react';
import {useParams} from 'react-router-dom';

import {Session} from '../pages/Session/Session';

export const SessionRoute: FC = () => {
  const {sessionId} = useParams();
  if (!sessionId) {
    throw new TypeError(`Missing session ID.`);
  }

  return <Session sessionID={sessionId} />;
};
