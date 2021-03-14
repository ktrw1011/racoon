import pickle
import shutil
from typing import Optional
from pathlib import Path

import pandas as pd


class ExpManager:
    def __init__(self,
        root_exp_dir:Optional[Path]=None,
        ) -> None:
        """[summary]

        Args:
            root_exp_dir (Optional[Path], optional): 実験ルートディレクトリ。デフォルトでカレントディレクトリ
            exp_name (Optional[str], optional): 実験名。デフォルトで
        """

        self.root_exp_dir = root_exp_dir
        if root_exp_dir is None:
            self.root_exp_dir= Path.cwd()
    
        self.version = self._exp_version()
        self.exp_dir = self.root_exp_dir / ('exp-' + self.version)

        # make features directory
        self.features_dir = self.exp_dir / 'features'
        self.features_dir.mkdir(exist_ok=True, parents=True)

        # make output directory
        self.output_dir = self.exp_dir / 'output'
        self.output_dir.mkdir(exist_ok=True, parents=True)

    def __repr__(self) -> str:
        return f"root experiment directory: {str(self.root_exp_dir)::>10}\n"\
            f"{'experiment version'}: {str(self.exp_dir.name):>10}\n"\
            f"{'features directory'}: {str(self.features_dir.stem):>10}\n"\
            f"{'output directory'}: {str(self.output_dir.stem):>10}\n"

    def _get_current_file_path(self) -> str:
        try:
            import ipynb_path
            return ipynb_path.get()
        except:
            raise ValueError

    def _exp_version(self) -> str:

        exps = list((self.root_exp_dir).glob('exp-*'))
        exps_dir = [p for p in exps if p.is_dir()]
        if len(exps_dir) == 0:
            return '0'
        else:
            vers = list(map(lambda x: int(str(x).split('-')[1]), exps_dir))
            vers = sorted(vers)[::-1][0]
        return str(int(vers)+1)

    def sweep(self, feature=True, output=True) -> None:
        if feature:
            shutil.rmtree(self.features_dir)
            self.features_dir.mkdir(exist_ok=False)
            print('[Swept Features Directory]')
        else:
            shutil.rmtree(self.output_dir)
            self.features_dir.mkdir(exist_ok=False)
            print('[Swept Output Directory]')

    def copy_current_file(self):
        pass

    def store_feature(self, name:str, input_df:pd.DataFrame) -> None:
        name = name + '.pkl'
        with open(self.features_dir / name, 'wb') as f:
            pickle.dump(input_df, f)

        print(f'[Save Feature]: {name}')

    def load_feature(self, name:str) -> pd.DataFrame:
        name = name + '.pkl'
        with open(self.features_dir / name, 'rb') as f:
            print(f'[Load Feature]: {name}')
            return pickle.load(f)

    def load_features(self) -> pd.DataFrame:
        _dfs = []
        for path in self.features_dir.glob('*.pkl'):
            with open(path, 'rb') as f:
                print(f'[Load Feature]: {path.name}')
                _dfs.append(pickle.load(f))

        return pd.concat(_dfs, axis=1)