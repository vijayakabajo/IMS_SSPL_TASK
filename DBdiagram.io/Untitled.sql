CREATE TABLE "supplier" (
  "id" integer PRIMARY KEY,
  "name" varchar(100),
  "contact_number" char(10),
  "status" boolean DEFAULT true
);

CREATE TABLE "item" (
  "id" integer PRIMARY KEY,
  "name" varchar(100),
  "quantity" integer,
  "price" decimal(10,2),
  "supplier_id" integer,
  "status" boolean DEFAULT true
);

COMMENT ON COLUMN "supplier"."contact_number" IS 'Validated as a 10-digit mobile number';

COMMENT ON COLUMN "supplier"."status" IS 'Pseudo delete, active or inactive';

COMMENT ON COLUMN "item"."price" IS 'Up to 10 digits with 2 decimal places';

COMMENT ON COLUMN "item"."status" IS 'Pseudo delete, active or inactive';

ALTER TABLE "item" ADD FOREIGN KEY ("supplier_id") REFERENCES "supplier" ("id");
