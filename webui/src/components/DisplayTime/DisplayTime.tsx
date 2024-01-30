import {FC, useEffect, useState} from 'react';

export type DisplayTimeProps = {
  timestamp: number;
};

const JUST_NOW = 1000 * 5;

export const DisplayTime: FC<DisplayTimeProps> = ({timestamp}) => {
  const [time, setTime] = useState(Date.now());
  const deltaNow = Math.max(0, time - timestamp);
  const isNow = deltaNow < JUST_NOW;

  useEffect(() => {
    const timeout = isNow
      ? setTimeout(
          () => setTime(Date.now()),
          Math.max(100, JUST_NOW - deltaNow + 100),
        )
      : undefined;
    return () => {
      clearInterval(timeout);
    };
  }, [isNow, deltaNow, setTime]);

  return isNow ? (
    <>Just now</>
  ) : (
    <>
      {new Date(timestamp).toLocaleString('en-US', {
        hour: 'numeric',
        minute: 'numeric',
        hour12: true,
      })}
    </>
  );
};
