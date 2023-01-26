<#
.SYNOPSIS
    Creates a Yara rule for search terms in an Excel spreadsheet column.
.DESCRIPTION
    This script will convert search terms in a column of an Excel
    spreadsheet into a Yara rule printed to stdout. It will assume
    the first row contains the title of the columns. Search terms will
    be picked up beginning in row 2.
.PARAMETER spreadsheet_filename
    The first parameter is the name of the Excel spreadsheet.
.PARAMETER term_column_number
    The number of the column that contains the term to search for.
.EXAMPLE
Excel2Yara.ps1 "C:\Download\Terms.xlsx" 1 >MyTerms.yara
    This will convert the cells in column one to a Yara rule. The output
    has been redirected to a file called "MyTerms.yara"
    Put that file into the "C:\ProgramData\Truxton" folder and it will
    automatically be used during Truxton exploitation.
.NOTES
        Author: Sam Blackburn (sblackburn@truxtonforensics.com)

        October 30, 2017 - Initial entry

        August 8, 2018 - Tried to get it to work with Excel 365 seeing how
        it differs from Excel 365

        August 17, 2018 - Gave up on Microsoft. They removed the 
        Excel.Application object from COM so Excel can no longer be used
        from Powershell.
#>

param
(
   [Parameter(Position=0,Mandatory=$true,HelpMessage="Please provide the spreadsheet filename.")][string] $spreadsheet_filename,
   [Parameter(Position=1,Mandatory=$true,HelpMessage="Please provide the column number of the search term.")][int] $term_column_number
)

if ( -NOT ( Test-Path $spreadsheet_filename ) )
{
   Write-Host $("The file named `"" + $spreadsheet_filename + "`" does not exist." )
   return;
}

if ( -NOT ( Test-Path -Path HKLM:SOFTWARE\Truxton -PathType Container ) )
{
   Write-Host $("Truxton doesn't seem to be installed. Registry key HKLM:SOFTWARE\Truxton is missing." )
   return;
}

$truxton_install_directory = Get-ItemProperty -Path HKLM:SOFTWARE\Truxton
Add-Type -Path $( $truxton_install_directory.InstallDirectory + "Client\Infragistics.WPF.Documents.Excel.dll" )

$workbook = [Infragistics.Documents.Excel.Workbook]::Load( $spreadsheet_filename )

if ( $workbook -EQ $null )
{
    Write-Output $("An unsupported version of Excel is on this system, can't get a workbook.")
    Return
}

$worksheets = $workbook.Worksheets

if ( $worksheets -EQ $null )
{
    Write-Output $("An unsupported version of Excel is on this system, can't get worksheets.")
    Return
}

$sheet = $worksheets.Item(0)

if ( $sheet -EQ $null )
{
    Write-Output $("Sheet is null.")
    Return
}

$rows = $sheet.Rows

$number_of_rows = $rows.Count

$cleaned_spreadsheet_name = $spreadsheet_filename -replace '\\','_'

$file_object = Get-ChildItem $spreadsheet_filename

Write-Output $("/*" )
Write-Output $("If you would like to automatically add other tags to any files that match, add them after the rule name like this:")
Write-Output $("rule Search_Terms : Tag1 Tag2 Tag3")
Write-Output $("*/")
Write-Output $("rule Search_Terms ")
Write-Output $("{")
Write-Output $(" meta:")

if ( $file_object -NE $null )
{
   Write-Output $("  description = `"Search terms from " + $cleaned_spreadsheet_name + " (last modified " + $file_object.LastWriteTime.ToShortDateString() + "). This file was generated " + (Get-Date).ToShortDateString() + "`"" )
}
else
{
   Write-Output $("  description = `"Search terms from " + $cleaned_spreadsheet_name + " This file was generated " + (Get-Date).ToShortDateString() + "`"" )
}

Write-Output $(" strings:")

# Start at Row 1 since Row 0 usually contains a column title like "All Search Terms"
for( $row_number = 1; $row_number -LT $number_of_rows; $row_number = $row_number + 1)
{
    $value = $sheet.Rows[$row_number].Cells[$term_column_number - 1].Value

    if ( $value -NE "" )
    {
        Write-Output $("  `$term" + $row_number + " = `"" + $value + "`"" )
    }
    else
    {
        $row_number = $rows.Count
    }
}

Write-Output $("")
Write-Output $(" condition:")
Write-Output $("  any of them")
Write-Output $("}")
Write-Output $("")

Write-Host $("Please save the above script to a file with a .yara extension then put an `"include`" directive in the `"" + $env:ProgramData + "\Truxton\Truxton.yara`" file.")
Write-Host $("For example, the `"" + $env:ProgramData + "\Truxton\Truxton.yara`" file should contain a line that looks like this:")

$yara_filename = [io.path]::GetFileNameWithoutExtension($spreadsheet_filename)
$yara_filename = $yara_filename + ".yara"
Write-Host $("include `"" + $yara_filename + "`"")
