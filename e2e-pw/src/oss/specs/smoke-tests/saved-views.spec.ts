import { describe } from "node:test";
import { expect, test } from "src/oss/fixtures";
import { getUniqueDatasetNameWithPrefix } from "src/oss/utils";

// test("smoke saved views", async ({ page, fiftyoneLoader }) => {
//   const datasetName = getUniqueDatasetNameWithPrefix("smoke-quickstart");

//   await fiftyoneLoader.loadZooDataset("quickstart", datasetName, {
//     max_samples: 5,
//   });

//   await fiftyoneLoader.waitUntilLoad(page, datasetName);

//   // await expect(page.getByTestId("entry-count-all")).toHaveText("5");
// });

describe("saved views", () => {
  const datasetName = getUniqueDatasetNameWithPrefix("smoke-quickstart");

  test.beforeAll(async ({ fiftyoneLoader }) => {
    await fiftyoneLoader.loadZooDataset("quickstart", datasetName, {
      max_samples: 5,
    });
  });

  test("has title", async ({ page, fiftyoneLoader }) => {
    await page.goto(`http://0.0.0.0:8787/datasets/${datasetName}`);

    await expect(page).toHaveTitle(/FiftyOne/);
  });

  test("saved views selector exist", async ({ page, fiftyoneLoader }) => {
    await page.goto(`http://0.0.0.0:8787/datasets/${datasetName}`);

    await fiftyoneLoader.waitUntilLoad(page, datasetName);
    const savedViewsLocator = page.getByText("Unsaved view");
    await expect(savedViewsLocator).toBeVisible();
  });

  test("saved views selector options opens and can create", async ({
    page,
    fiftyoneLoader,
  }) => {
    await page.goto(`http://0.0.0.0:8787/datasets/${datasetName}`);

    await fiftyoneLoader.waitUntilLoad(page, datasetName);
    await page.getByText("Unsaved view").click();

    const savedViewsCreate = await page.getByText(
      "save current filters as view"
    );
    await expect(savedViewsCreate).toBeVisible();
    await expect(savedViewsCreate).not.toBeDisabled();
  });
});
