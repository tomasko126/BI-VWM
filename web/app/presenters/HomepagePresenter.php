<?php

declare(strict_types=1);

namespace App\Presenters;

use App\Model\InvertedModel;
use App\Model\SequentialModel;
use Nette;

final class HomepagePresenter extends Nette\Application\UI\Presenter {

    // @var InvertedModel
    private $invertedModel;

    // @var SequentialModel
    private $sequentialModel;

    public function injectDependencies(InvertedModel $invertedModel, SequentialModel $sequentialModel) {
        $this->invertedModel = $invertedModel;
        $this->sequentialModel = $sequentialModel;
    }

    public function renderDefault() {
        $randomChosenId = $this->invertedModel->getOneRandomDocument();
        $this->template->randomDocumentId = $randomChosenId;
    }
}