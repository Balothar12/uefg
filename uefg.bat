@echo off
IF "%UEFG_SCRIPT_LOCATION%" == "" (
    ECHO "error: unset script location"
) ELSE (
    CALL python "%UEFG_SCRIPT_LOCATION%" %*
)