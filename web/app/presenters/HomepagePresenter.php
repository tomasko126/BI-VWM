<?php

declare(strict_types=1);

namespace App\Presenters;

use App\Model\DocumentsModel;
use Nette;

final class HomepagePresenter extends Nette\Application\UI\Presenter {

    // @var DocumentsModel
    private $documentsModel;

    public function injectDependencies(DocumentsModel $documentsModel) {
        $this->documentsModel = $documentsModel;
    }

    public function actionDefault() {
        $randomChosenId = $this->documentsModel->getOneRandomDocument();
        $this->redirect('Search:inverted', $randomChosenId);
    }
}