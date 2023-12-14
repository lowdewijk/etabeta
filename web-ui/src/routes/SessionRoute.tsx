import {FC} from 'react';
import {useParams} from 'react-router-dom';

import {Session} from '../pages/Session/Session';

export const SessionRoute: FC = () => {
  const {id} = useParams();
  const idn = Number.parseInt(id ?? '');
  if (Number.isNaN(idn)) {
    return <p>Invalid session ID</p>;
  }

  return <Session id={idn} />;
};
