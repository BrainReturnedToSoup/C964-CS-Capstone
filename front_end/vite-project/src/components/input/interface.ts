export interface Input_Interface {
  id: string;
  label: string;
  name: string;
  defaultVal: string;
  isValid: boolean;
  constrainErrorMessage: string;
  onChange: (e: React.SyntheticEvent) => void;
}
