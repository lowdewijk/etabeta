import {DependencyList, useCallback, useEffect, useRef} from 'react';
import {matchPath, PathMatch, PathPattern, useLocation} from 'react-router-dom';
import {isEqual} from 'lodash';

type EnterProps = {prevPathMatch: undefined; pathMatch: PathMatch<string>};
type ChangeProps = {
  prevPathMatch: PathMatch<string>;
  pathMatch: PathMatch<string>;
};
type LeaveProps = {prevPathMatch: PathMatch<string>; pathMatch: undefined};
type OnUpdateProps = EnterProps | ChangeProps | LeaveProps;

/**
 * A hook that allows you to listen to path changes in the URL.
 * @param pathPattern a react-router v6 path pattern
 * @param onUpdate a function that is called when you enter, leave or change the path
 * @param deps dependencies for the onUpdate function
 */
export const useRoutePathUpdate = (
  pathPattern: PathPattern<string> | string,
  onUpdate: (props: OnUpdateProps) => void,
  deps: DependencyList,
) => {
  const location = useLocation();
  const pathMatch = matchPath(pathPattern, location.pathname);
  const prevPathMatch = useRef<PathMatch<string> | null>(null);
  // eslint-disable-next-line react-hooks/exhaustive-deps
  const onUpdateCallback = useCallback(onUpdate, deps);

  useEffect(() => {
    if (pathMatch) {
      if (prevPathMatch.current === null) {
        onUpdateCallback({prevPathMatch: undefined, pathMatch});
      } else if (!isEqual(prevPathMatch.current, pathMatch)) {
        onUpdateCallback({prevPathMatch: prevPathMatch.current, pathMatch});
      }
    } else if (prevPathMatch.current !== null) {
      onUpdateCallback({
        prevPathMatch: prevPathMatch.current,
        pathMatch: undefined,
      });
    }
    prevPathMatch.current = pathMatch;
  }, [pathMatch, prevPathMatch, onUpdateCallback]);
};
