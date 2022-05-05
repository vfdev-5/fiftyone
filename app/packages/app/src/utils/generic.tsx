import React from "react";
import mime from "mime";
import styled from "styled-components";
import { useExternalLink, prettify as pretty } from "@fiftyone/utilities";
import { matchPath } from "@fiftyone/components";

export const isFloat = (n: number): boolean => {
  return Number(n) === n && n % 1 !== 0;
};

const Link = styled.a`
  color: ${({ theme }) => theme.font};
`;

export const ExternalLink = ({ href, ...props }) => {
  const onClick = useExternalLink(href);
  return <Link {...props} href={href} target="_blank" onClick={onClick} />;
};

export const prettify = (
  v: boolean | string | null | undefined | number | number[]
): React.ReactNode => {
  const result = pretty(v);

  if (result instanceof URL) {
    const url = result.toString();
    return (
      <ExternalLink title={url} href={url}>
        {url}
      </ExternalLink>
    );
  }

  return v;
};

export const genSort = (a, b, asc) => {
  if (a === b) {
    return 0;
  }

  if (a === null) {
    return 1;
  }

  if (b === null) {
    return -1;
  }

  if (a > b) {
    return asc ? 1 : -1;
  }

  return asc ? -1 : 1;
};

export const getMimeType = (sample: any) => {
  return (
    (sample.metadata && sample.metadata.mime_type) ||
    mime.getType(sample.filepath) ||
    "image/jpg"
  );
};

export const formatDateTime = (timeStamp: number, timeZone: string): string => {
  const twoDigit = "2-digit";
  const MS = 1000;
  const S = 60 * MS;
  const M = 60 * S;
  const H = 24 * M;

  const options: Intl.DateTimeFormatOptions = {
    timeZone,
    year: "numeric",
    day: twoDigit,
    month: twoDigit,
    hour: twoDigit,
    hour12: false,
    minute: twoDigit,
    second: twoDigit,
    // @ts-ignore
    fractionalSecondDigits: 3,
  };

  if (!(timeStamp % MS)) {
    // @ts-ignore
    delete options.fractionalSecondDigits;
  }

  if (!(timeStamp % H)) {
    delete options.second;
    delete options.minute;
    delete options.hour;
  }

  return new Intl.DateTimeFormat("en-ZA", options)
    .format(timeStamp)
    .replaceAll("/", "-")
    .replace(", ", " ")
    .replace(",", ".");
};

export const getDateTimeRangeFormattersWithPrecision = (() => {
  const twoDigit = "2-digit";
  let locale = "en-ZA";

  const MS = 1000;
  const S = 60 * MS;
  const M = 60 * S;
  const H = 24 * M;

  return (
    timeZone: string,
    d1: number,
    d2: number
  ): [Intl.DateTimeFormat | null, Intl.DateTimeFormat] => {
    const delta = Math.abs(d1 - d2);
    let common: Intl.DateTimeFormatOptions = { timeZone, hour12: false };
    let diff: Intl.DateTimeFormatOptions = {
      timeZone,
      hour12: false,
    };

    if (d1 % H === 0 && d2 % H === 0) {
      common = null;
      diff = {
        year: "numeric",
        month: twoDigit,
        day: twoDigit,
      };
      locale = "en-CA";
    } else if (delta < MS) {
      common = {
        year: "numeric",
        day: twoDigit,
        month: twoDigit,
      };
      diff = {
        hour: twoDigit,
        minute: twoDigit,
        second: twoDigit,
        // @ts-ignore
        fractionalSecondDigits: 3,
      };
      locale = "en-ZA";
    } else if (delta < S) {
      common = {
        year: "numeric",
        day: twoDigit,
        month: twoDigit,
        hour: twoDigit,
        minute: twoDigit,
      };
      diff = {
        second: twoDigit,
        // @ts-ignore
        fractionalSecondDigits: 3,
      };
      locale = "en-ZA";
    } else if (delta < M) {
      common = {
        year: "numeric",
        day: twoDigit,
        month: twoDigit,
      };
      diff = {
        hour: twoDigit,
        minute: twoDigit,
        second: twoDigit,
      };
      locale = "en-ZA";
    } else {
      common = null;
      diff = {
        year: "numeric",
        month: twoDigit,
        day: twoDigit,
        hour: twoDigit,
        minute: twoDigit,
        second: twoDigit,
      };
      locale = "en-ZA";
    }

    return [
      common ? new Intl.DateTimeFormat(locale, common) : null,
      new Intl.DateTimeFormat(locale, diff),
    ];
  };
})();

export const getDatasetName = (): string => {
  const result = matchPath(window.location.pathname, {
    path: "/datasets/:name",
    exact: true,
    defaultParams: {},
  });

  if (result) {
    return result.params.name();
  }

  return null;
};
