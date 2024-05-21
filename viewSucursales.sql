CREATE VIEW ViewSucursales AS
SELECT calldate, src, dst, billsec, disposition,
'M' AS branch FROM sucursalMochis.cdr
UNION ALL
SELECT calldate, src, dst, billsec, disposition,
'N' AS branch FROM sucursalNavojoa.cdr
UNION ALL
SELECT calldate, src, dst, billsec, disposition,
'O' AS branch FROM sucursalObregon.cdr;
