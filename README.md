# Data Engineering Solution for Web Analytics

Extract and Load data from an API to AWS Bucket. Then integrate, transform, and automate the data in Snowflake.

![](src/amplitude_extract_diagram.png)
_figure 1_

## Extract: Move data from Amplitude API to an AWS S3 Bucket

---

**Make an API Call**

Make a GET Request that saves the result to memory.

**Decompress files files**

Unzip .zip and .gz files and copy contents into a output location.

**Other Features**

- **Logging**: Store logs when running on local machine.
- **Parameterization**: Accept parameters instead of a hardcoded values.
- **Functional Decomposition**: Split functions into single purpose sub-functions.
- **Cloud Storage**: Upload files into an S3 Bucket
- **Transformation**: Transform json into structure data

## Transform: Medallion Architecture

### 🥉 Bronze layer

Parse multiple layers of json.

### 🥈 Silver Layer

[View Entity Relationship Diagram]()

**Base table**

The base table is a set of fields that are returned by the [Amplitude Export API](). Each field was evaluated and a list of excluded fields is noted in the transformation_test.sql.

**Dimension tables**

These are the dimension tables:

- Locations
- Users
- Events

With the exception of Events which has `event_id` as its primary key, surrogate keys are generated using the MD5 algorithm to create a unique and deterministic identifier for the table.

```sql
select
	md5(concat(
        coalesce(cast(country), ''),
        coalesce(cast(region), '')
        coalesce(cast(city), '')
        )
    ) as location_id
from amplitude_base
```

**Fact Table**

Fact tables contain foreign keys to the dimension tables. As mentioned above, Events were identified with the event_id that is produced from Amplitude's API. However, the Location and User dimensions have surrogate keys generated with the md5 algorithm. Intentionally, MD5 has inconsistent value returns, so the surrogate key cannot simply be regenerated the same way it was in the dimension tables. Instead, we will join the dimension tables to the fact table to select the proper foreign key.

```sql
select
    event_id
    ...
    , l.location_id
from amplitude_base as b
left join dim_amplitude_locations as u
    on b.country = u.country
    and b.region = u.region
    and b.city = u.city
```

### 🥇 Gold Layer

## Planned Improvements

---

- **How users can get started**: Installation/setup instructions with usage examples
- **Where users can get help**: Support resources and documentation links
- **Who maintains and contributes**: Maintainer information and contribution guidelines
