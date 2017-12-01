-- How to update a table
-- How to declare variables
-- How to update variables
-- How to get first of month or last day of month
-- How to get Monday/Sunday of previous week
-- How to get monday of current week
-- How to create a temp table
-- How to insert into a table
-- How to insert into a table from another table
-- How to join two tables
-- How to select n number of rows
-- How to select rows in ascending order
-- How to select rows in descending order
-- How to select unique vales (no dups)
-- How to write IF statements
-- How to write Loops
-- How to write a case statement within an update
-- How to check for NULL values
-- How to write an update statement with a sub query
-- How to use the Keyword "IN"
-- How to count all of the rows in a table
-- How to delete contents of a table
-- How to select the smallest/largest value in a column
-- How to pause for n number of seconds
-- How to string match
-- How to dynaically select a column using a CASE statement
-- How to unhighlight key words
-- How to permanently delete a table
-- How to do perform a boolean check
-- How to use the length function
-- How to check if column is numberic
-- How to find tables in database
-- How to find columns in database


/***************************************************************************************************************************************************/

-- you usually put this at the top of your code
-- means all tables you are referencing are inside this database
USE DBname

/*Example

-- using the USE keyword
USE NY
SELECT * FROM tblCustomer

-- without USE keyword
SELECT * FROM NY.dbo.tblCustomer

*/

/***************************************************************************************************************************************************/

-- How to update a table

--ver1:
UPDATE tblName
	SET Column1 = 1,
	Column2 = 'NERevenueCode',
	Column3 = getdate()
WHERE Column4 = 'NEAccSummaryLoadMain'

--ver2:
UPDATE cc
	SET cc.Column1 = 1,
	cc.Column2 = 'NERevenueCode',
	cc.Column3 = getdate()
FROM tblName cc
WHERE cc.Column4 = 'NEAccSummaryLoadMain'


/***************************************************************************************************************************************************/

-- How to declare variables

Declare @Var1 datetime
Declare @Var2 char(20)
Declare @Var3 nvarchar(20)
Declare @Var4 int
Declare @Var5 decimal (18,2)
Declare @Var6 bit


/***************************************************************************************************************************************************/

-- How to update variables

Declare @BeginDate datetime
	Set @BeginDate = getdate() -- gets todays date

SELECT @BeginDate -- select variable


/***************************************************************************************************************************************************/

--Function COALESCE (Var1, Var2, ....)
-- This function returns first variable that is not null


/***************************************************************************************************************************************************/

-- Date functions
SELECT getdate() -- Todays date with time stamp
SELECT dateadd (dd, datediff (dd, 0, GetDate()), 0) --Todays date with no time stamp 
SELECT dateadd (dd, datediff (dd, 0, GetDate()), -1) --Yesterdays date with no time stamp 
SELECT DateAdd (yy, -1, DateDiff(dd, 0, GetDate())) --One year ago no timestamp

/***************************************************************************************************************************************************/

-- How to get first of month or last day of month

--Declare variables
Declare @BeginDate datetime
Declare @EndDate datetime

-- set @BeginDate = first day of last month
Set @BeginDate = DateAdd(mm, DateDiff(mm, 0, GetDate()) - 1, 0)

-- set @EndDate = last day of last month
Set @EndDate = DateAdd(dd, -1, (DateAdd(mm, 1, @BeginDate)))

SELECT @BeginDate as BeginDate, @EndDate as EndDate 

/***************************************************************************************************************************************************/

-- How to get Monday/Sunday of previous week

--Declare variables
Declare @BeginDate datetime
Declare @EndDate datetime
Declare @StartDate datetime

SET @StartDate =        -- get monday of current week
CASE WHEN DATENAME(dw,GETDATE()) = 'Monday'
      THEN DATEADD(dd, 0,DATEDIFF(dd, 0,(DATEADD(dd, 0, GETDATE()))))
      WHEN DATENAME(dw,GETDATE()) = 'Tuesday'
      THEN DATEADD(dd, 0,DATEDIFF(dd, 0,(DATEADD(dd, -1, GETDATE()))))
      WHEN DATENAME(dw,GETDATE()) = 'Wednesday'
      THEN DATEADD(dd, 0,DATEDIFF(dd, 0,(DATEADD(dd, -2, GETDATE()))))
      WHEN DATENAME(dw,GETDATE()) = 'Thursday'
      THEN DATEADD(dd, 0,DATEDIFF(dd, 0,(DATEADD(dd, -3, GETDATE()))))
      WHEN DATENAME(dw,GETDATE()) = 'Friday'
      THEN DATEADD(dd, 0,DATEDIFF(dd, 0,(DATEADD(dd, -4, GETDATE()))))
      WHEN DATENAME(dw,GETDATE()) = 'Saturday'
      THEN DATEADD(dd, 0,DATEDIFF(dd, 0,(DATEADD(dd, -5, GETDATE()))))
      WHEN DATENAME(dw,GETDATE()) = 'Sunday'
      THEN DATEADD(dd, 0,DATEDIFF(dd, 0,(DATEADD(dd, -6, GETDATE()))))
ELSE (DATEADD(dd, 0, GETDATE()))
END

-- set @BeginDate = monday of previous week
Set @BeginDate = dateadd(dd,datediff(dd,0,@StartDate),-7)

-- set @EndDate = sunday of previous week
Set @EndDate = dateadd(dd,datediff(dd,0,@BeginDate),6)



/***************************************************************************************************************************************************/


-- How to create a temp table

IF OBJECT_ID('tempdb..#tblName','u') IS NOT NULL
BEGIN
DROP TABLE #tblName
END
CREATE TABLE #tblName 
(
	Var1 varchar (25) PRIMARY KEY,
	Var2 datetime
)

/***************************************************************************************************************************************************/


-- How to insert into a table

IF OBJECT_ID('tempdb..#tblName','u') IS NOT NULL
BEGIN
DROP TABLE #tblName
END
CREATE TABLE #tblName 
(
	Var1 varchar (25) PRIMARY KEY,
	Var2 datetime
)

INSERT #tblName (Var1, Var2)
SELECT 'tom',
		getdate() 

SELECT * FROM #tblName

/***************************************************************************************************************************************************/

-- How to insert into a table from another table


IF OBJECT_ID('tempdb..#tblName','u') IS NOT NULL
BEGIN
DROP TABLE #tblName
END
CREATE TABLE #tblName 
(
	Var1 varchar (25) PRIMARY KEY,
	Var2 datetime
)

IF OBJECT_ID('tempdb..#tblName2','u') IS NOT NULL
BEGIN
DROP TABLE #tblName2
END
CREATE TABLE #tblName2
(
	Var1 varchar (25) PRIMARY KEY,
	Var2 datetime
)

INSERT #tblName2 (Var1, Var2)
SELECT 'tom',
		getdate() 

INSERT #tblName (Var1, Var2)		
SELECT Var1,
		Var2
FROM #tblName2	

SELECT * FROM #tblName

/***************************************************************************************************************************************************/

-- How to join two tables

-- Only returns if col1 matches col2
SELECT a.*
FROM tbl1 a
JOIN tbl2 b on (a.Col1 = b.Col2)

-- Returns all rows from tbl1 even if col1 does not match col2
SELECT a.*
FROM tbl1 a
LEFT JOIN tbl2 b on (a.Col1 = b.Col2)

/***************************************************************************************************************************************************/

-- selects only n number of rows
-- does not mean they will be in asc or desc order
SELECT top 500 Col1
FROM tbl1

/***************************************************************************************************************************************************/

-- Select rows in ascending order
SELECT *
FROM tbl1
ORDER BY Col1 ASC

-- Select rows in descending order
SELECT *
FROM tbl1
ORDER BY Col1 DESC

/***************************************************************************************************************************************************/

-- select unique vales (no dups)
SELECT DISTINCT Col1
FROM tbl1

/***************************************************************************************************************************************************/

-- IF statements

IF (SELECT @Var1) = 1
	BEGIN
		SELECT @Var2
	END
ELSE
	BEGIN
		SELECT @Var3
	END
	
/***************************************************************************************************************************************************/

-- Loops

DECLARE @Boundary varchar(25)
SET @Boundary = (SELECT MAX(Var1) FROM tblName)

WHILE @Boundary IS NOT NULL
BEGIN


-- do stuff here


SET @Boundary = (SELECT MAX(Var1) FROM tblName WHERE Var1 < @Boundary)
END


/***************************************************************************************************************************************************/

-- case statement within an update
UPDATE dr
      SET dr.Col1 =
			CASE
				WHEN (SELECT @Var1) > 0 THEN 'Residential'
				ELSE 'Commercial'
			END
      FROM tblName dr
      
/***************************************************************************************************************************************************/

-- How to check for NULL values


--function ISNULL (Var1, 0)	
-- if Var1 is null then assign it a zero, or whatever you want
SELECt ISNULL (Col1, 0) FROM tblName

-- you can also just check the column without modifying it
SELECT * 
FROM tblName
WHERE Col1 IS NOT NULL -- select everything where Col1 is not null

SELECT * 
FROM tblName
WHERE Col1 IS NULL -- select everything where Col1 is null

/***************************************************************************************************************************************************/

-- update statement with a sub query
UPDATE dr2
SET dr2.Col1 =(SELECT ISNULL (SUM (cl.Col2),0)
				   FROM	tblName2 cl
				   WHERE cl.Col3 = dr2.Col5
				   AND cl.col8 IN (5, 6, 7)
				  )

FROM tblName dr2


/***************************************************************************************************************************************************/


-- "IN" keyword is used a lot
Update dr
Set dr.Col1 = ISNULL(
	(SELECT SUM(Col3) FROM tblName1 WHERE col10 = dr.Col5 AND
		Col4 IN ('GrossReceiptsTax', 'SalesTax', 'TexasSalesTax', 'TexasGrossReceiptsTax')),0) -- IN() can have any number of parameters
From tblName2 dr 

/***************************************************************************************************************************************************/


-- How to count all the rows in a table
SELECT COUNT(*) FROM tblName

/***************************************************************************************************************************************************/

-- How to delete contents of a table

DELETE tblName -- deletes all contents of table


DELETE tblName -- deletes only rows where col1 = 0
WHERE col1 = 0

/***************************************************************************************************************************************************/

-- How to select the smallest/largest value in a column
SELECT MIN (col1) FROM tblName
SELECT MAX (col1) FROM tblName

/***************************************************************************************************************************************************/

-- How to pause for n number of seconds
WAITFOR DELAY '00:00:10' -- 10 sec

/***************************************************************************************************************************************************/

-- How to string match

SELECT * 
FROM tblName
WHERE Col1 LIKE '%StringYouAreSearchingFor%' 

SELECT * 
FROM tblName
WHERE Col1 NOT LIKE '%StringYouAreSearchingFor%'

/***************************************************************************************************************************************************/

-- How to dynaically select a column using a CASE statement

DECLARE @Column varchar(25)
SET @Column = 'Tax'

SELECT *
FROM tblName
WHERE Col1 = 'NJ'
AND (CASE @Column
		WHEN 'Misc' THEN DB.dbo.tblName.Col2
		WHEN 'Tax' THEN DB.dbo.tblName.Col3
		WHEN 'Market' THEN DB.dbo.tblName.Col4
		WHEN 'Variance' THEN DB.dbo.tblName.Col5
	END) <> 0

/***************************************************************************************************************************************************/

-- How to unhighlight key words

-- example using "state"
-- Notice that the column state is a keyword so sql will highlight it
-- I have not seen a problem leaving it like this
SELECT state FROM tblName

-- Put in brackets to unhighlight
SELECT [state] FROM tblName

/***************************************************************************************************************************************************/

-- How to permanently delete a table

DROP TABLE tblName

/***************************************************************************************************************************************************/

-- How to do perform a boolean check

-- if tblName is empty the if statement will fail
IF EXISTS (SELECT * FROM tblName)
BEGIN
	-- do stuff here
END

-- query will return results if tblName2 is not empty
SELECT * 
FROM tblName
WHERE EXISTS (SELECT * FROM tblName2)

/***************************************************************************************************************************************************/

-- How to use the length function

-- Fix bad zip codes
UPDATE ne
Set ne.ZipCode = '00000'
FROM tblName ne
WHERE len (ne.Zipcode) <> 5 -- zipcode smaller/grater than 5 digits long

/***************************************************************************************************************************************************/

-- How to check if column is numberic

UPDATE ne
Set ne.ZipCode = '00000'
FROM tblName ne
WHERE ISNUMERIC (ne.Zipcode) = 0 -- zipcode has non numeric characters

/***************************************************************************************************************************************************/

-- How to find tables in database

SELECT * 
FROM DB.INFORMATION_SCHEMA.Columns 
WHERE TABLE_NAME LIKE '%TableNameYouAreLookingFor%' -- where DB is the name of the database you are searching in


/***************************************************************************************************************************************************/

-- How to find columns in database

SELECT * 
FROM DB.INFORMATION_SCHEMA.Columns 
WHERE COLUMN_NAME LIKE '%ColumnNameYouAreLookingFor%' -- where DB is the name of the database you are searching in


/***************************************************************************************************************************************************/

