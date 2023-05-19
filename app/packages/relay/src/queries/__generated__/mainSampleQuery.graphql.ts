/**
<<<<<<< HEAD
 * @generated SignedSource<<5dd66d8bb092f30a878ecc8d1737dd8d>>
=======
 * @generated SignedSource<<db6c5e51a0149510460a52970649c85f>>
>>>>>>> ca44d57e9 (modal network request)
 * @lightSyntaxTransform
 * @nogrep
 */

/* tslint:disable */
/* eslint-disable */
// @ts-nocheck

import { ConcreteRequest, Query } from 'relay-runtime';
export type SampleFilter = {
  group?: GroupElementFilter | null;
  id?: string | null;
};
export type GroupElementFilter = {
  id?: string | null;
  slice?: string | null;
};
export type mainSampleQuery$variables = {
  dataset: string;
  filter: SampleFilter;
  view: Array;
};
export type mainSampleQuery$data = {
  readonly sample: {
    readonly __typename: "ImageSample";
    readonly id: string;
    readonly sample: object;
    readonly urls: ReadonlyArray<{
      readonly field: string;
      readonly url: string | null;
    }>;
  } | {
    readonly __typename: "VideoSample";
    readonly frameRate: number;
    readonly id: string;
    readonly sample: object;
    readonly urls: ReadonlyArray<{
      readonly field: string;
      readonly url: string | null;
    }>;
  } | {
    // This will never be '%other', but we need some
    // value in case none of the concrete values match.
    readonly __typename: "%other";
  } | null;
};
export type mainSampleQuery = {
  response: mainSampleQuery$data;
  variables: mainSampleQuery$variables;
};

const node: ConcreteRequest = (function(){
var v0 = {
  "defaultValue": null,
  "kind": "LocalArgument",
  "name": "dataset"
},
v1 = {
  "defaultValue": null,
  "kind": "LocalArgument",
  "name": "filter"
},
v2 = {
  "defaultValue": null,
  "kind": "LocalArgument",
  "name": "view"
},
v3 = [
  {
    "kind": "Variable",
    "name": "dataset",
    "variableName": "dataset"
  },
  {
    "kind": "Variable",
    "name": "filter",
    "variableName": "filter"
  },
  {
    "kind": "Variable",
    "name": "view",
    "variableName": "view"
  }
],
v4 = {
  "alias": null,
  "args": null,
  "kind": "ScalarField",
  "name": "__typename",
  "storageKey": null
},
v5 = {
  "alias": null,
  "args": null,
  "kind": "ScalarField",
  "name": "id",
  "storageKey": null
},
v6 = {
  "alias": null,
  "args": null,
  "kind": "ScalarField",
  "name": "sample",
  "storageKey": null
},
v8 = {
  "alias": null,
  "args": null,
  "concreteType": "MediaURL",
  "kind": "LinkedField",
  "name": "urls",
  "plural": true,
  "selections": [
    {
      "alias": null,
      "args": null,
      "kind": "ScalarField",
      "name": "field",
      "storageKey": null
    },
    {
      "alias": null,
      "args": null,
      "kind": "ScalarField",
      "name": "url",
      "storageKey": null
    }
  ],
  "storageKey": null
},
<<<<<<< HEAD
v7 = {
  "kind": "InlineFragment",
  "selections": [
    (v4/*: any*/),
    (v5/*: any*/),
    (v6/*: any*/)
=======
v9 = {
  "kind": "InlineFragment",
  "selections": [
    (v6/*: any*/),
    (v7/*: any*/),
    (v8/*: any*/)
>>>>>>> ca44d57e9 (modal network request)
  ],
  "type": "ImageSample",
  "abstractKey": null
},
<<<<<<< HEAD
v8 = {
  "kind": "InlineFragment",
  "selections": [
    (v4/*: any*/),
    (v5/*: any*/),
=======
v10 = {
  "kind": "InlineFragment",
  "selections": [
    (v6/*: any*/),
    (v7/*: any*/),
>>>>>>> ca44d57e9 (modal network request)
    {
      "alias": null,
      "args": null,
      "kind": "ScalarField",
      "name": "frameRate",
      "storageKey": null
    },
<<<<<<< HEAD
    (v6/*: any*/)
=======
    (v8/*: any*/)
>>>>>>> ca44d57e9 (modal network request)
  ],
  "type": "VideoSample",
  "abstractKey": null
};
return {
  "fragment": {
    "argumentDefinitions": [
      (v0/*: any*/),
      (v1/*: any*/),
      (v2/*: any*/)
    ],
    "kind": "Fragment",
    "metadata": null,
    "name": "mainSampleQuery",
    "selections": [
      {
        "alias": null,
        "args": (v3/*: any*/),
        "concreteType": null,
        "kind": "LinkedField",
        "name": "sample",
        "plural": false,
        "selections": [
<<<<<<< HEAD
          (v7/*: any*/),
          (v8/*: any*/)
=======
          (v5/*: any*/),
          (v9/*: any*/),
          (v10/*: any*/)
>>>>>>> ca44d57e9 (modal network request)
        ],
        "storageKey": null
      }
    ],
    "type": "Query",
    "abstractKey": null
  },
  "kind": "Request",
  "operation": {
    "argumentDefinitions": [
      (v0/*: any*/),
      (v2/*: any*/),
      (v1/*: any*/)
    ],
    "kind": "Operation",
    "name": "mainSampleQuery",
    "selections": [
      {
        "alias": null,
        "args": (v3/*: any*/),
        "concreteType": null,
        "kind": "LinkedField",
        "name": "sample",
        "plural": false,
        "selections": [
<<<<<<< HEAD
          {
            "alias": null,
            "args": null,
            "kind": "ScalarField",
            "name": "__typename",
            "storageKey": null
          },
          (v7/*: any*/),
          (v8/*: any*/),
          {
            "kind": "InlineFragment",
            "selections": [
              (v4/*: any*/)
=======
          (v5/*: any*/),
          (v9/*: any*/),
          (v10/*: any*/),
          {
            "kind": "InlineFragment",
            "selections": [
              (v6/*: any*/)
>>>>>>> ca44d57e9 (modal network request)
            ],
            "type": "PointCloudSample",
            "abstractKey": null
          }
        ],
        "storageKey": null
      }
    ]
  },
  "params": {
    "cacheID": "8288bef45852588e173f7ad9366b1cbc",
    "id": null,
    "metadata": {},
    "name": "mainSampleQuery",
    "operationKind": "query",
    "text": "query mainSampleQuery(\n  $dataset: String!\n  $view: BSONArray!\n  $filter: SampleFilter!\n) {\n  sample(dataset: $dataset, view: $view, filter: $filter) {\n    __typename\n    ... on ImageSample {\n      id\n      sample\n      urls {\n        field\n        url\n      }\n    }\n    ... on VideoSample {\n      id\n      sample\n      frameRate\n      urls {\n        field\n        url\n      }\n    }\n    ... on PointCloudSample {\n      id\n    }\n  }\n}\n"
  }
};
})();

<<<<<<< HEAD
(node as any).hash = "20386ac4db1c242b8eda0747ef22faa1";
=======
(node as any).hash = "0d109ba0bd7d1a9df954199a1af114be";
>>>>>>> ca44d57e9 (modal network request)

export default node;
